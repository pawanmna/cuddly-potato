"""
Configuration Settings for Blockchain File Sharing System
"""

import os


class Config:
    """
    Application configuration
    """
    
    # IPFS Settings
    IPFS_API_URL = os.getenv("IPFS_API_URL", "http://127.0.0.1:5001")
    IPNS_LIFETIME = "24h"  # How long IPNS records are valid
    
    # Blockchain Settings
    BLOCKCHAIN_DIFFICULTY = 0  # Mining difficulty (0 = instant)
    
    # File Storage Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BLOCKCHAIN_DATA_DIR = os.path.join(BASE_DIR, "blockchain_data")
    BLOCKCHAIN_FILE = os.path.join(BLOCKCHAIN_DATA_DIR, "blockchain.json")
    ENCRYPTION_KEY_FILE = os.path.join(BLOCKCHAIN_DATA_DIR, "encryption.key")
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
    
    # Flask Settings
    FLASK_HOST = "127.0.0.1"
    FLASK_PORT = 5000
    FLASK_DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB max file size
    
    # Security
    ALLOWED_EXTENSIONS = None  # None = allow all file types


def get_config():
    """
    Get configuration instance
    
    Returns:
        Config instance
    """
    return Config()


if __name__ == "__main__":
    # Display configuration
    config = Config()
    
    print("=" * 60)
    print("CONFIGURATION")
    print("=" * 60)
    print(f"\nIPFS Settings:")
    print(f"  API URL: {config.IPFS_API_URL}")
    print(f"  IPNS Lifetime: {config.IPNS_LIFETIME}")
    
    print(f"\nBlockchain Settings:")
    print(f"  Difficulty: {config.BLOCKCHAIN_DIFFICULTY}")
    
    print(f"\nFile Storage:")
    print(f"  Blockchain File: {config.BLOCKCHAIN_FILE}")
    print(f"  Encryption Key: {config.ENCRYPTION_KEY_FILE}")
    print(f"  Upload Folder: {config.UPLOAD_FOLDER}")
    print(f"  Download Folder: {config.DOWNLOAD_FOLDER}")
    
    print(f"\nFlask Settings:")
    print(f"  Host: {config.FLASK_HOST}")
    print(f"  Port: {config.FLASK_PORT}")
    print(f"  Debug: {config.FLASK_DEBUG}")
    print(f"  Max Upload Size: {config.MAX_CONTENT_LENGTH / (1024*1024)} MB")
