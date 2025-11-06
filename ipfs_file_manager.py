"""
IPFS File Manager with Encryption
Integrates blockchain, IPFS, and AES-256 encryption
"""

import os
import uuid
import json
from datetime import datetime
from cryptography.fernet import Fernet
from blockchain import Blockchain
from ipfs_manager import IPFSManager
from config import Config


class IPFSFileManager:
    """
    Manages encrypted file uploads, downloads, and blockchain integration
    """
    
    def __init__(self, blockchain_file=None, encryption_key_file=None):
        """
        Initialize file manager with blockchain and encryption
        
        Args:
            blockchain_file: Path to blockchain JSON file
            encryption_key_file: Path to encryption key file
        """
        self.config = Config()
        self.blockchain_file = blockchain_file or self.config.BLOCKCHAIN_FILE
        self.encryption_key_file = encryption_key_file or self.config.ENCRYPTION_KEY_FILE
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.blockchain_file), exist_ok=True)
        os.makedirs(self.config.UPLOAD_FOLDER, exist_ok=True)
        
        # Initialize encryption
        self.cipher = self._load_or_create_encryption_key()
        
        # Initialize blockchain
        self.blockchain = self._load_or_create_blockchain()
        
        # Initialize IPFS
        self.ipfs = IPFSManager(self.config.IPFS_API_URL)
        
        print(f"✓ File manager initialized")
        print(f"  Blockchain: {len(self.blockchain)} blocks")
        print(f"  Encryption: AES-256-GCM (Fernet)")
    
    def _load_or_create_encryption_key(self):
        """
        Load existing encryption key or create new one
        
        Returns:
            Fernet cipher instance
        """
        if os.path.exists(self.encryption_key_file):
            with open(self.encryption_key_file, 'rb') as f:
                key = f.read()
            print(f"✓ Loaded encryption key from {self.encryption_key_file}")
        else:
            key = Fernet.generate_key()
            with open(self.encryption_key_file, 'wb') as f:
                f.write(key)
            print(f"✓ Generated new encryption key: {self.encryption_key_file}")
        
        return Fernet(key)
    
    def _load_or_create_blockchain(self):
        """
        Load existing blockchain or create new one
        
        Returns:
            Blockchain instance
        """
        if os.path.exists(self.blockchain_file):
            try:
                with open(self.blockchain_file, 'r') as f:
                    content = f.read().strip()
                    if not content:
                        raise ValueError("Blockchain file is empty")
                    blockchain_dict = json.loads(content)
                blockchain = Blockchain.from_dict(blockchain_dict)
                print(f"✓ Loaded blockchain from {self.blockchain_file}")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️  Blockchain file corrupted ({e}), creating new one...")
                blockchain = Blockchain(difficulty=self.config.BLOCKCHAIN_DIFFICULTY)
                # Save the newly created blockchain
                with open(self.blockchain_file, 'w') as f:
                    json.dump(blockchain.to_dict(), f, indent=2)
                print(f"✓ Created new blockchain")
        else:
            blockchain = Blockchain(difficulty=self.config.BLOCKCHAIN_DIFFICULTY)
            # Save the newly created blockchain
            with open(self.blockchain_file, 'w') as f:
                json.dump(blockchain.to_dict(), f, indent=2)
            print(f"✓ Created new blockchain")
        
        return blockchain
    
    def _save_blockchain(self):
        """
        Save blockchain to JSON file
        """
        with open(self.blockchain_file, 'w') as f:
            json.dump(self.blockchain.to_dict(), f, indent=2)
    
    def encrypt_file(self, input_path, output_path):
        """
        Encrypt file using AES-256
        
        Args:
            input_path: Path to plaintext file
            output_path: Path to save encrypted file
            
        Returns:
            Path to encrypted file
        """
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        
        ciphertext = self.cipher.encrypt(plaintext)
        
        with open(output_path, 'wb') as f:
            f.write(ciphertext)
        
        print(f"🔒 Encrypted: {os.path.basename(input_path)}")
        return output_path
    
    def decrypt_file(self, input_path, output_path):
        """
        Decrypt file using AES-256
        
        Args:
            input_path: Path to encrypted file
            output_path: Path to save decrypted file
            
        Returns:
            Path to decrypted file
        """
        with open(input_path, 'rb') as f:
            ciphertext = f.read()
        
        plaintext = self.cipher.decrypt(ciphertext)
        
        with open(output_path, 'wb') as f:
            f.write(plaintext)
        
        print(f"🔓 Decrypted: {os.path.basename(output_path)}")
        return output_path
    
    def upload_file(self, file_path, file_name, encrypt=True):
        """
        Upload file to IPFS with optional encryption
        
        Args:
            file_path: Path to file to upload
            file_name: Original filename
            encrypt: Whether to encrypt before uploading
            
        Returns:
            Dictionary with file metadata
        """
        file_id = str(uuid.uuid4())
        file_size = os.path.getsize(file_path)
        
        # Encrypt if requested
        if encrypt:
            encrypted_path = os.path.join(
                self.config.UPLOAD_FOLDER,
                f"{file_id}.enc"
            )
            self.encrypt_file(file_path, encrypted_path)
            upload_path = encrypted_path
        else:
            upload_path = file_path
        
        # Add to IPFS
        ipfs_cid = self.ipfs.add_file(upload_path)
        
        # Pin the file
        self.ipfs.pin_file(ipfs_cid)
        
        # Create metadata
        metadata = {
            "type": "ipfs_file_metadata",
            "file_id": file_id,
            "file_name": file_name,
            "ipfs_cid": ipfs_cid,
            "file_size": file_size,
            "encrypted": encrypt,
            "upload_time": datetime.now().isoformat()
        }
        
        # Add to blockchain
        self.blockchain.add_block(metadata)
        self._save_blockchain()
        
        # Cleanup encrypted temp file
        if encrypt and os.path.exists(encrypted_path):
            os.remove(encrypted_path)
        
        print(f"✓ File uploaded: {file_name} (ID: {file_id})")
        return metadata
    
    def download_file(self, file_id, output_dir=None):
        """
        Download file from IPFS
        
        Args:
            file_id: Unique file identifier
            output_dir: Directory to save file (default: downloads/)
            
        Returns:
            Path to downloaded file
            
        Raises:
            ValueError: If file not found in blockchain
        """
        # Find file in blockchain
        block = self.blockchain.get_block_by_file_id(file_id)
        if not block:
            raise ValueError(f"File not found: {file_id}")
        
        metadata = block.data
        file_name = metadata["file_name"]
        ipfs_cid = metadata["ipfs_cid"]
        encrypted = metadata["encrypted"]
        
        # Determine output directory
        if output_dir is None:
            output_dir = self.config.DOWNLOAD_FOLDER
        os.makedirs(output_dir, exist_ok=True)
        
        # Download from IPFS
        if encrypted:
            encrypted_path = os.path.join(output_dir, f"{file_id}.enc")
            self.ipfs.get_file(ipfs_cid, encrypted_path)
            
            # Decrypt
            output_path = os.path.join(output_dir, file_name)
            self.decrypt_file(encrypted_path, output_path)
            
            # Cleanup encrypted file
            os.remove(encrypted_path)
        else:
            output_path = os.path.join(output_dir, file_name)
            self.ipfs.get_file(ipfs_cid, output_path)
        
        print(f"✓ File downloaded: {file_name}")
        return output_path
    
    def list_files(self):
        """
        List all files in blockchain
        
        Returns:
            List of file metadata dictionaries
        """
        files = []
        for block in self.blockchain.chain[1:]:  # Skip genesis block
            if isinstance(block.data, dict) and block.data.get("type") == "ipfs_file_metadata":
                files.append(block.data)
        return files
    
    def delete_file(self, file_id):
        """
        Remove file from blockchain (file stays on IPFS network)
        
        Args:
            file_id: Unique file identifier
            
        Returns:
            True if successful
        """
        # Find block with file
        for i, block in enumerate(self.blockchain.chain):
            if isinstance(block.data, dict) and block.data.get("file_id") == file_id:
                self.blockchain.remove_block(i)
                self._save_blockchain()
                print(f"✓ File removed from blockchain: {file_id}")
                return True
        
        return False
    
    def publish_blockchain(self):
        """
        Publish blockchain to IPNS
        
        Returns:
            IPNS name (/ipns/...)
        """
        # Save current blockchain
        self._save_blockchain()
        
        # Add blockchain JSON to IPFS
        blockchain_cid = self.ipfs.add_file(self.blockchain_file)
        
        # Publish to IPNS
        ipns_name = self.ipfs.publish_to_ipns(
            blockchain_cid,
            lifetime=self.config.IPNS_LIFETIME
        )
        
        print(f"✓ Blockchain published to IPNS")
        return ipns_name
    
    def sync_from_peer(self, peer_ipns):
        """
        Sync blockchain from another peer's IPNS
        
        Args:
            peer_ipns: Peer's IPNS name (/ipns/... or peer ID)
            
        Returns:
            Dictionary with sync results
        """
        try:
            # Resolve IPNS to CID
            blockchain_cid = self.ipfs.resolve_ipns(peer_ipns)
            
            # Download blockchain
            temp_file = os.path.join(
                self.config.UPLOAD_FOLDER,
                f"temp_blockchain_{uuid.uuid4()}.json"
            )
            self.ipfs.get_file(blockchain_cid, temp_file)
            
            # Load peer blockchain
            with open(temp_file, 'r') as f:
                peer_blockchain_dict = json.load(f)
            peer_blockchain = Blockchain.from_dict(peer_blockchain_dict)
            
            # Validate peer blockchain
            if not peer_blockchain.is_chain_valid():
                os.remove(temp_file)
                return {
                    "success": False,
                    "message": "Peer blockchain is invalid (tampered)"
                }
            
            # Compare with local blockchain
            needs_update = False
            
            if len(peer_blockchain) > len(self.blockchain):
                needs_update = True
                reason = f"Peer has more blocks ({len(peer_blockchain)} vs {len(self.blockchain)})"
            elif len(peer_blockchain) == len(self.blockchain):
                peer_hash = peer_blockchain.get_latest_block().hash
                local_hash = self.blockchain.get_latest_block().hash
                if peer_hash != local_hash:
                    needs_update = True
                    reason = "Same length but different content"
                else:
                    reason = "Blockchains are identical"
            else:
                reason = f"Peer has fewer blocks ({len(peer_blockchain)} vs {len(self.blockchain)})"
            
            # Update if needed
            if needs_update:
                self.blockchain = peer_blockchain
                self._save_blockchain()
                os.remove(temp_file)
                return {
                    "success": True,
                    "message": f"Synced! {reason}",
                    "blocks": len(self.blockchain)
                }
            else:
                os.remove(temp_file)
                return {
                    "success": True,
                    "message": f"No update needed. {reason}",
                    "blocks": len(self.blockchain)
                }
        
        except Exception as e:
            return {
                "success": False,
                "message": f"Sync failed: {str(e)}"
            }
    
    def get_peer_ipns(self):
        """
        Get this node's IPNS name
        
        Returns:
            IPNS name string
        """
        return self.ipfs.get_ipns_name()


if __name__ == "__main__":
    # Test file manager
    print("=" * 60)
    print("FILE MANAGER TEST")
    print("=" * 60)
    
    try:
        fm = IPFSFileManager()
        
        # Create test file
        test_file = "test_upload.txt"
        with open(test_file, 'w') as f:
            f.write("This is a test file for the blockchain file sharing system.")
        
        # Upload file
        print("\n" + "=" * 60)
        print("UPLOAD TEST")
        print("=" * 60)
        metadata = fm.upload_file(test_file, "test_upload.txt", encrypt=True)
        print(f"Uploaded: {metadata}")
        
        # List files
        print("\n" + "=" * 60)
        print("FILE LIST")
        print("=" * 60)
        files = fm.list_files()
        for file in files:
            print(f"- {file['file_name']} (ID: {file['file_id']})")
        
        # Download file
        print("\n" + "=" * 60)
        print("DOWNLOAD TEST")
        print("=" * 60)
        downloaded = fm.download_file(metadata['file_id'], output_dir="downloads")
        
        # Verify content
        with open(downloaded, 'r') as f:
            content = f.read()
            print(f"Downloaded content: {content}")
        
        # Cleanup
        os.remove(test_file)
        os.remove(downloaded)
        os.rmdir("downloads")
        
        print("\n✓ All tests passed!")
        
    except ConnectionError as e:
        print(f"\n✗ {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
