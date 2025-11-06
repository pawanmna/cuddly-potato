# Blockchain File Sharing System - Project Instructions

## Project Overview
Decentralized file sharing system combining blockchain and IPFS technologies.

## Technology Stack
- **Backend**: Python 3.8+, Flask
- **Blockchain**: Custom implementation with SHA-256
- **Storage**: IPFS (InterPlanetary File System)
- **Encryption**: AES-256-GCM (Fernet)
- **Frontend**: HTML5, JavaScript, Bootstrap 5

## Project Structure
- `blockchain.py` - Block and Blockchain classes
- `ipfs_manager.py` - IPFS operations (add, get, publish, resolve)
- `ipfs_file_manager.py` - File management with encryption
- `web_app.py` - Flask server and REST API
- `config.py` - Configuration settings
- `templates/index.html` - Web interface
- `blockchain_data/` - Local blockchain and encryption key storage
- `uploads/` - Temporary file upload directory

## Key Features
- Immutable blockchain record keeping
- Decentralized IPFS file storage
- End-to-end AES-256 encryption
- IPNS for persistent addressing
- P2P device synchronization
- Web-based interface

## Development Guidelines
- Use SHA-256 for all block hashing
- Blockchain difficulty set to 0 (instant mining)
- IPNS lifetime: 24 hours
- Always validate blockchain before syncing
- Encrypt files before IPFS upload
- Use proper error handling for network operations
