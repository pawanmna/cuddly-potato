import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from web.app import app, config, init_file_manager
import traceback


if __name__ == '__main__':
    print("=" * 60)
    print("BLOCKCHAIN FILE SHARING SYSTEM")
    print("=" * 60)
    print()
    
    try:
        # Initialize file manager
        fm = init_file_manager()
        
        print()
        print("=" * 60)
        print("YOUR IPNS ADDRESS")
        print("=" * 60)
        ipns = fm.get_peer_ipns()
        print(f"\n{ipns}\n")
        print("Share this address with other devices to sync files!")
        print()
        
        print("=" * 60)
        print("STARTING WEB SERVER")
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
        print("STARTUP FAILED")
        print("=" * 60)
        print(f"\n{e}\n")
        print("Please ensure IPFS daemon is running:")
        print("  $ ipfs daemon")
        print()
    except KeyboardInterrupt:
        print("\n\nServer stopped")
    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print(f"\n{e}\n")
        traceback.print_exc()
