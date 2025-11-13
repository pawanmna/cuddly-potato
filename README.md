# Blockchain File Sharing System

Decentralized file sharing with IPFS, blockchain, and AES-256 encryption.


## Quick Start

1. **Install IPFS**: [ipfs.tech/install](https://docs.ipfs.tech/install/)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Start IPFS**: `ipfs daemon`
4. **Run app**: `python run.py`
5. **Open**: [http://localhost:5000](http://localhost:5000)

## Usage Guide

### Upload Files

1. Drag & Drop files onto the upload area, or click to browse
2. Check “Encrypt files” to enable AES-256 encryption (recommended)
3. Click “Upload Files”
4. Files are encrypted → added to IPFS → recorded in blockchain

### Share Files (Publishing)

1. Click “Publish to IPNS”
2. Wait 30–60 seconds for DHT propagation
3. Copy your IPNS address (shown at top of page)
4. Share this IPNS with other devices

### Receive Files (Syncing)

**On the receiving device:**

1. Get the sender’s IPNS address
2. Paste it into “Receive Files from Peer” section
3. Click “Sync Blockchain”
4. Files from sender will appear in your file list
5. Click “Download” to retrieve files

### Download Files

1. Click the “Download” button next to any file
2. File is downloaded from IPFS → decrypted → saved to Downloads folder

