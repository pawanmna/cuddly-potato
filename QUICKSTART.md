# 🚀 QUICK START GUIDE

## Complete Setup in 3 Steps

### ✅ Prerequisites Installed
- ✓ Python 3.14 virtual environment configured
- ✓ Flask, requests, cryptography installed
- ⚠️ **IPFS still needs to be installed separately**

---

## 📦 Step 1: Install IPFS

### Option A: Download Official Release
1. Visit: https://docs.ipfs.tech/install/
2. Download Kubo for Windows
3. Extract and add to PATH

### Option B: Quick Install (Windows)
```powershell
# Download and install using chocolatey
choco install kubo

# Or download directly
# https://dist.ipfs.tech/#kubo
```

### Verify Installation
```powershell
ipfs --version
# Should show: ipfs version 0.38.2 or higher
```

### Initialize IPFS (First Time Only)
```powershell
ipfs init
```

---

## 🎯 Step 2: Start IPFS Daemon

**Open PowerShell Terminal #1:**

```powershell
ipfs daemon
```

**Wait for this message:**
```
Daemon is ready
```

**Keep this terminal open!** IPFS must run continuously.

---

## 🌐 Step 3: Start the Application

**Open PowerShell Terminal #2:**

```powershell
cd C:\Users\hp\Documents\something_new

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start Flask server
python web_app.py
```

**You should see:**

```
🔗 BLOCKCHAIN FILE SHARING SYSTEM
✓ Connected to IPFS (version 0.38.2)
✓ File manager initialized

📍 YOUR IPNS ADDRESS
/ipns/12D3KooWxxxxxxxx...

🚀 STARTING WEB SERVER
Web Interface: http://127.0.0.1:5000
```

---

## 🎉 Step 4: Open Web Interface

Open your browser to: **http://localhost:5000**

---

## 📝 Quick Usage

### Upload a File
1. Drag & drop file onto upload area
2. Click "Upload Files"
3. File is encrypted and added to IPFS

### Share with Another Device
1. Click "📤 Publish to IPNS"
2. Copy your IPNS address (shown at top)
3. Share with other device

### Sync from Another Device
1. Get sender's IPNS address
2. Paste in "Receive Files from Peer"
3. Click "🔄 Sync Blockchain"
4. Files appear in your list

### Download a File
1. Click download button next to file
2. File downloads to your Downloads folder

---

## 🐛 Common Issues

### "Cannot connect to IPFS daemon"
**Solution:** Make sure `ipfs daemon` is running in separate terminal

### "Module not found" errors
**Solution:** Activate virtual environment first:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Port already in use
**Solution:** Change port in `config.py`:
```python
FLASK_PORT = 5001  # or any free port
```

---

## 📂 Project Structure

```
something_new/
├── blockchain.py              # Blockchain logic
├── ipfs_manager.py           # IPFS operations
├── ipfs_file_manager.py      # File encryption/management
├── web_app.py                # Flask server (RUN THIS)
├── config.py                 # Settings
├── requirements.txt          # Dependencies
├── README.md                 # Full documentation
├── templates/
│   └── index.html           # Web UI
└── .venv/                   # Python virtual environment
```

---

## 🎓 What You Built

This is a **production-ready decentralized file sharing system** featuring:

- ✅ Blockchain with SHA-256 hashing
- ✅ IPFS decentralized storage
- ✅ AES-256 file encryption
- ✅ Peer-to-peer synchronization
- ✅ Modern web interface
- ✅ REST API

**Perfect for:**
- Academic projects
- Portfolio demonstrations
- Learning blockchain/IPFS
- Decentralized app development

---

## 🆘 Need Help?

1. **Check logs** in both terminals for errors
2. **Read full docs** in `README.md`
3. **Test individual modules:**
   ```powershell
   python blockchain.py      # Test blockchain
   python ipfs_manager.py    # Test IPFS (daemon must be running)
   python ipfs_file_manager.py  # Test encryption
   ```

---

## 🎯 Next Steps

- Read the complete guide in your prompt
- Experiment with multi-device sync
- Explore the code to understand how it works
- Try modifying the blockchain difficulty
- Add custom features

---

**Built with ❤️ using Blockchain, IPFS, and Python**

🔗 **Decentralized • Encrypted • Peer-to-Peer**
