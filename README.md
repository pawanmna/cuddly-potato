# 🔗 Blockchain File Sharing System

A **decentralized file sharing system** that combines blockchain technology and IPFS (InterPlanetary File System) to create an immutable, encrypted, peer-to-peer file distribution network.

## 🌟 Features

- ✅ **Decentralized Storage** - Files stored on IPFS network, not central servers
- ✅ **Blockchain Records** - Immutable file metadata using SHA-256 hashing
- ✅ **End-to-End Encryption** - AES-256-GCM encryption for all files
- ✅ **Peer-to-Peer Sync** - Share files directly between devices using IPNS
- ✅ **Web Interface** - Modern, responsive UI with drag-and-drop upload
- ✅ **No Central Authority** - Fully decentralized, no single point of failure

## 🏗️ Architecture

```
┌──────────────┐
│  Web Browser │
└──────┬───────┘
       │ HTTP
┌──────▼───────┐      ┌──────────────┐      ┌──────────────┐
│ Flask Server │◄────►│  Blockchain  │      │  Encryption  │
└──────┬───────┘      └──────────────┘      └──────────────┘
       │                                            │
       │                                            │
┌──────▼───────┐      ┌──────────────┐             │
│ IPFS Manager │◄────►│  IPFS Daemon │◄────────────┘
└──────────────┘      └──────┬───────┘
                             │
                      ┌──────▼───────┐
                      │ Global IPFS  │
                      │   Network    │
                      └──────────────┘
```

## 📋 Prerequisites

### 1. Python 3.8+

```bash
python --version
# Should be 3.8 or higher
```

### 2. IPFS (Kubo)

**Download and Install:**

- **Official**: https://docs.ipfs.tech/install/
- **Or use included**: `kubo_v0.38.2_linux-amd64.tar.gz` (Linux) or download for your OS

**Installation Steps:**

```bash
# Extract Kubo (Linux/Mac)
tar -xvzf kubo_v0.38.2_linux-amd64.tar.gz
cd kubo
sudo bash install.sh

# Verify installation
ipfs --version
```

**Windows**: Download `.zip` from https://dist.ipfs.tech/#kubo and extract to PATH

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Clone or navigate to project directory
cd something_new

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Start IPFS Daemon

**Terminal 1:**

```bash
# Initialize IPFS (first time only)
ipfs init

# Start IPFS daemon
ipfs daemon
```

Wait for: `Daemon is ready`

### Step 3: Start the Application

**Terminal 2:**

```bash
# Start Flask web server
python web_app.py
```

You should see:

```
✓ Connected to IPFS (version 0.38.2)
✓ Loaded blockchain from blockchain_data/blockchain.json
✓ File manager initialized

📍 YOUR IPNS ADDRESS
/ipns/12D3KooW...

🚀 STARTING WEB SERVER
Web Interface: http://127.0.0.1:5000
```

### Step 4: Open Web Interface

Open your browser to: **http://localhost:5000**

## 📖 Usage Guide

### Upload Files

1. **Drag & Drop** files onto the upload area, or click to browse
2. Check **"Encrypt files"** to enable AES-256 encryption (recommended)
3. Click **"Upload Files"**
4. Files are encrypted → added to IPFS → recorded in blockchain

### Share Files (Publishing)

1. Click **"📤 Publish to IPNS"**
2. Wait 30-60 seconds for DHT propagation
3. **Copy your IPNS address** (shown at top of page)
4. Share this IPNS with other devices

### Receive Files (Syncing)

**On the receiving device:**

1. Get the sender's IPNS address
2. Paste it into **"Receive Files from Peer"** section
3. Click **"🔄 Sync Blockchain"**
4. Files from sender will appear in your file list
5. Click **Download** to retrieve files

### Download Files

1. Click the **Download** button next to any file
2. File is downloaded from IPFS → decrypted → saved to Downloads folder

## 🔧 Project Structure

```
something_new/
├── blockchain.py              # Blockchain implementation
├── ipfs_manager.py           # IPFS operations
├── ipfs_file_manager.py      # File management + encryption
├── web_app.py                # Flask server & REST API
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web interface
├── blockchain_data/
│   ├── blockchain.json      # Local blockchain storage
│   └── encryption.key       # AES-256 encryption key
└── uploads/                 # Temporary upload directory
```

## 🔐 How It Works

### 1. File Upload Flow

```
User uploads file
    ↓
Encrypt with AES-256
    ↓
Add to IPFS → Get CID
    ↓
Create blockchain block with metadata
    ↓
Save blockchain locally
```

### 2. Blockchain Structure

Each block contains:

```python
{
    "index": 1,
    "timestamp": 1699276800.123,
    "data": {
        "type": "ipfs_file_metadata",
        "file_id": "unique-uuid",
        "file_name": "document.pdf",
        "ipfs_cid": "QmXxxx...",
        "file_size": 1048576,
        "encrypted": true
    },
    "previous_hash": "abc123...",
    "hash": "def456...",  # SHA-256
    "nonce": 0
}
```

### 3. Publishing Flow

```
Blockchain → JSON file
    ↓
Add JSON to IPFS → Get CID
    ↓
Publish CID to IPNS (24h lifetime)
    ↓
IPNS name: /ipns/12D3KooW...
```

### 4. Syncing Flow

```
Enter peer's IPNS
    ↓
Resolve IPNS → Get blockchain CID
    ↓
Download blockchain from IPFS
    ↓
Validate chain integrity
    ↓
Compare with local blockchain
    ↓
Update if peer has newer/different blocks
```

### 5. Download Flow

```
Select file from list
    ↓
Get IPFS CID from blockchain
    ↓
Download encrypted file from IPFS
    ↓
Decrypt with local key
    ↓
Save to Downloads folder
```

## 🔑 Security

### Encryption

- **Algorithm**: AES-256-GCM (via Fernet)
- **Key Storage**: Local only (`blockchain_data/encryption.key`)
- **Key Sharing**: NOT automatic (by design)

⚠️ **Important**: Each device has its own encryption key. You can only decrypt files you uploaded, unless you manually share the encryption key.

### Blockchain Integrity

- **SHA-256 hashing** for all blocks
- **Chain validation** before syncing
- **Tamper detection** via hash verification

## 🌐 API Reference

### GET /api/peer-id

Get this node's IPNS address.

**Response:**

```json
{
  "success": true,
  "ipns": "/ipns/12D3KooW..."
}
```

### POST /api/upload

Upload files to IPFS and blockchain.

**Form Data:**

- `files`: File(s) to upload
- `encrypt`: "true" or "false"

**Response:**

```json
{
  "success": true,
  "uploaded": [...],
  "count": 2
}
```

### GET /api/files

List all files in blockchain.

**Response:**

```json
{
  "success": true,
  "files": [
    {
      "file_id": "abc-123",
      "file_name": "document.pdf",
      "ipfs_cid": "QmXxxx...",
      "file_size": 1048576,
      "encrypted": true,
      "upload_time": "2025-11-06T12:00:00"
    }
  ],
  "count": 1
}
```

### GET /api/download/\<file_id\>

Download file from IPFS.

**Response:** File download

### POST /api/delete/\<file_id\>

Delete file from blockchain.

**Response:**

```json
{
  "success": true,
  "message": "File removed from blockchain"
}
```

### POST /api/publish

Publish blockchain to IPNS.

**Response:**

```json
{
  "success": true,
  "ipns": "/ipns/12D3KooW...",
  "message": "Blockchain published to IPNS"
}
```

### POST /api/sync

Sync blockchain from peer.

**Request Body:**

```json
{
  "peer_ipns": "/ipns/12D3KooW... or peer_id"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Synced! Peer has more blocks (3 vs 2)",
  "blocks": 3
}
```

### GET /api/blockchain

Get blockchain data.

**Response:**

```json
{
  "success": true,
  "blockchain": {...},
  "blocks": 3,
  "valid": true
}
```

## 🐛 Troubleshooting

### Problem: "Cannot connect to IPFS daemon"

**Solution:**

```bash
# Start IPFS daemon in separate terminal
ipfs daemon
```

### Problem: "Both devices show same IPNS"

**Cause**: Using same IPFS repository

**Solution** (on ONE device):

```bash
# Stop daemon
Ctrl+C

# Backup and reinitialize
mv ~/.ipfs ~/.ipfs.backup
ipfs init
ipfs daemon
```

### Problem: "Failed to resolve IPNS"

**Solutions:**

1. Wait 60 seconds after publishing (DHT propagation)
2. Connect devices directly:

```bash
# Device 1: Get peer address
ipfs id

# Device 2: Connect directly
ipfs swarm connect /ip4/192.168.1.100/tcp/4001/p2p/12D3Koo...
```

### Problem: "Sync shows 'up to date' but files missing"

**Solution**: Restart both IPFS daemons to clear cache

### Problem: "Decryption error"

**Cause**: Different encryption keys on devices

**Note**: By design! You can only decrypt files you uploaded. To share encrypted files, you must manually share the encryption key file.

## 🧪 Testing

### Test Blockchain

```bash
python blockchain.py
```

### Test IPFS Manager

```bash
python ipfs_manager.py
```

### Test File Manager

```bash
python ipfs_file_manager.py
```

## ⚙️ Configuration

Edit `config.py` to customize:

```python
class Config:
    IPFS_API_URL = "http://127.0.0.1:5001"
    IPNS_LIFETIME = "24h"
    BLOCKCHAIN_DIFFICULTY = 0  # 0 = instant mining
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100 MB
    FLASK_PORT = 5000
```

## 📚 Technologies Used

| Technology      | Purpose                          |
| --------------- | -------------------------------- |
| **Python**      | Backend programming              |
| **Flask**       | Web server and REST API          |
| **IPFS (Kubo)** | Decentralized file storage       |
| **Blockchain**  | Immutable record keeping         |
| **SHA-256**     | Cryptographic hashing            |
| **AES-256**     | File encryption (Fernet)         |
| **IPNS**        | Persistent peer addressing       |
| **Bootstrap 5** | Responsive web interface         |
| **JavaScript**  | Frontend interactivity           |

## 📝 Use Cases

- 📖 Academic research data sharing
- 🎓 Educational blockchain/IPFS demonstrations
- 🔐 Censorship-resistant file distribution
- 💼 Decentralized document management
- 🧪 Distributed systems experimentation

## 🤝 Contributing

This is an educational project demonstrating blockchain and IPFS concepts. Feel free to extend it!

**Potential improvements:**

- Multi-device encryption key sharing
- File versioning
- Smart contracts integration
- Mobile app interface
- Advanced blockchain consensus
- IPFS cluster support

## ⚠️ Limitations

- Encryption keys are NOT automatically shared between devices
- Files remain on IPFS network even after "deletion" from blockchain
- IPNS resolution can be slow (30-60 seconds)
- No built-in access control or permissions
- Suitable for educational/experimental use

## 📄 License

This project is provided as-is for educational purposes.

## 🆘 Support

For issues:

1. Check IPFS daemon is running: `ipfs daemon`
2. Check Flask server is running: `python web_app.py`
3. Review terminal logs for error messages
4. Verify IPFS version: `ipfs --version` (recommended: 0.38.2+)

---

**Built with ❤️ using Blockchain, IPFS, and Python**

🔗 **Decentralized • Encrypted • Peer-to-Peer**
