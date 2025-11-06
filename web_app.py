"""
Flask Web Application for Blockchain File Sharing System
Provides REST API and web interface
"""

from flask import Flask, request, jsonify, render_template, send_file
import os
import traceback
from werkzeug.utils import secure_filename
from ipfs_file_manager import IPFSFileManager
from config import Config

# Initialize Flask app
app = Flask(__name__)
config = Config()
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

# Initialize file manager
file_manager = None


def init_file_manager():
    """
    Initialize file manager (lazy loading)
    """
    global file_manager
    if file_manager is None:
        try:
            file_manager = IPFSFileManager()
        except ConnectionError as e:
            print(f"✗ Failed to initialize: {e}")
            raise
    return file_manager


# ============================================================================
# WEB ROUTES
# ============================================================================

@app.route('/')
def index():
    """
    Render main web interface
    """
    return render_template('index.html')


# ============================================================================
# API ROUTES
# ============================================================================

@app.route('/api/peer-id', methods=['GET'])
def get_peer_id():
    """
    Get this node's IPNS address
    
    Returns:
        JSON: {"ipns": "/ipns/..."}
    """
    try:
        fm = init_file_manager()
        ipns = fm.get_peer_ipns()
        return jsonify({
            "success": True,
            "ipns": ipns
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_files():
    """
    Upload files to IPFS and add to blockchain
    
    Form Data:
        files: File(s) to upload
        encrypt: "true" or "false" (optional, default: true)
    
    Returns:
        JSON: {"success": true, "uploaded": [...]}
    """
    try:
        fm = init_file_manager()
        
        # Check if files present
        if 'files' not in request.files:
            return jsonify({
                "success": False,
                "error": "No files provided"
            }), 400
        
        files = request.files.getlist('files')
        encrypt = request.form.get('encrypt', 'true').lower() == 'true'
        
        uploaded = []
        
        for file in files:
            if file.filename == '':
                continue
            
            # Save uploaded file temporarily
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(temp_path)
            
            # Upload to IPFS and blockchain
            metadata = fm.upload_file(temp_path, filename, encrypt=encrypt)
            uploaded.append(metadata)
            
            # Remove temp file
            os.remove(temp_path)
        
        return jsonify({
            "success": True,
            "uploaded": uploaded,
            "count": len(uploaded)
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/files', methods=['GET'])
def list_files():
    """
    List all files in blockchain
    
    Returns:
        JSON: {"success": true, "files": [...]}
    """
    try:
        fm = init_file_manager()
        files = fm.list_files()
        
        return jsonify({
            "success": True,
            "files": files,
            "count": len(files)
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/download/<file_id>', methods=['GET'])
def download_file(file_id):
    """
    Download file from IPFS
    
    Args:
        file_id: Unique file identifier
    
    Returns:
        File download
    """
    try:
        fm = init_file_manager()
        
        # Download file
        file_path = fm.download_file(file_id, output_dir=config.DOWNLOAD_FOLDER)
        
        # Send file to user
        return send_file(
            file_path,
            as_attachment=True,
            download_name=os.path.basename(file_path)
        )
    
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 404
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/delete/<file_id>', methods=['POST', 'DELETE'])
def delete_file(file_id):
    """
    Delete file from blockchain
    
    Args:
        file_id: Unique file identifier
    
    Returns:
        JSON: {"success": true/false}
    """
    try:
        fm = init_file_manager()
        success = fm.delete_file(file_id)
        
        if success:
            return jsonify({
                "success": True,
                "message": "File removed from blockchain"
            })
        else:
            return jsonify({
                "success": False,
                "error": "File not found"
            }), 404
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/publish', methods=['POST'])
def publish_blockchain():
    """
    Publish blockchain to IPNS
    
    Returns:
        JSON: {"success": true, "ipns": "...", "cid": "..."}
    """
    try:
        fm = init_file_manager()
        result = fm.publish_blockchain()
        
        return jsonify({
            "success": True,
            "ipns": result["ipns"],
            "cid": result["cid"],
            "message": "Blockchain published! Use CID for faster sync."
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/sync', methods=['POST'])
def sync_blockchain():
    """
    Sync blockchain from peer's IPNS
    
    JSON Body:
        {"peer_ipns": "/ipns/..." or "peer_id"}
    
    Returns:
        JSON: {"success": true/false, "message": "..."}
    """
    try:
        fm = init_file_manager()
        
        data = request.get_json()
        if not data or 'peer_ipns' not in data:
            return jsonify({
                "success": False,
                "error": "Missing peer_ipns in request"
            }), 400
        
        peer_ipns = data['peer_ipns'].strip()
        
        result = fm.sync_from_peer(peer_ipns)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 500
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/blockchain', methods=['GET'])
def get_blockchain():
    """
    Get blockchain data
    
    Returns:
        JSON: {"success": true, "blockchain": {...}}
    """
    try:
        fm = init_file_manager()
        
        return jsonify({
            "success": True,
            "blockchain": fm.blockchain.to_dict(),
            "blocks": len(fm.blockchain),
            "valid": fm.blockchain.is_chain_valid()
        })
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(413)
def request_entity_too_large(error):
    """
    Handle file too large error
    """
    max_size_mb = config.MAX_CONTENT_LENGTH / (1024 * 1024)
    return jsonify({
        "success": False,
        "error": f"File too large. Maximum size: {max_size_mb} MB"
    }), 413


@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors
    """
    return jsonify({
        "success": False,
        "error": "Resource not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """
    Handle 500 errors
    """
    return jsonify({
        "success": False,
        "error": "Internal server error"
    }), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🔗 BLOCKCHAIN FILE SHARING SYSTEM")
    print("=" * 60)
    print()
    
    try:
        # Initialize file manager
        fm = init_file_manager()
        
        print()
        print("=" * 60)
        print("📍 YOUR IPNS ADDRESS")
        print("=" * 60)
        ipns = fm.get_peer_ipns()
        print(f"\n{ipns}\n")
        print("Share this address with other devices to sync files!")
        print()
        
        print("=" * 60)
        print("🚀 STARTING WEB SERVER")
        print("=" * 60)
        print(f"\nWeb Interface: http://{config.FLASK_HOST}:{config.FLASK_PORT}")
        print()
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        print()
        
        # Start Flask server
        app.run(
            host=config.FLASK_HOST,
            port=config.FLASK_PORT,
            debug=config.FLASK_DEBUG
        )
    
    except ConnectionError as e:
        print()
        print("=" * 60)
        print("✗ STARTUP FAILED")
        print("=" * 60)
        print(f"\n{e}\n")
        print("Please ensure IPFS daemon is running:")
        print("  $ ipfs daemon")
        print()
    except KeyboardInterrupt:
        print("\n\n✓ Server stopped")
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ ERROR")
        print("=" * 60)
        print(f"\n{e}\n")
        traceback.print_exc()
