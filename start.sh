#!/bin/bash

# Blockchain File Sharing System - Startup Script (Linux/Mac)

echo "========================================================"
echo "🔗 BLOCKCHAIN FILE SHARING SYSTEM - STARTUP"
echo "========================================================"
echo ""

# Check if IPFS is installed
if ! command -v ipfs &> /dev/null
then
    echo "✗ IPFS is not installed!"
    echo ""
    echo "Please install IPFS from: https://docs.ipfs.tech/install/"
    echo "Or extract the included kubo package"
    exit 1
fi

echo "✓ IPFS found: $(ipfs --version)"

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "✗ Python 3 is not installed!"
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if dependencies are installed
echo ""
echo "Checking Python dependencies..."
python3 -c "import flask, requests, cryptography" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Missing dependencies. Installing..."
    pip3 install -r requirements.txt
else
    echo "✓ All dependencies installed"
fi

# Initialize IPFS if not already initialized
if [ ! -d "$HOME/.ipfs" ]; then
    echo ""
    echo "Initializing IPFS..."
    ipfs init
fi

echo ""
echo "========================================================"
echo "Starting IPFS Daemon..."
echo "========================================================"
echo ""

# Start IPFS daemon in background
ipfs daemon > /dev/null 2>&1 &
IPFS_PID=$!

# Wait for IPFS to be ready
sleep 3

# Check if IPFS is running
if ps -p $IPFS_PID > /dev/null 2>&1; then
    echo "✓ IPFS daemon started (PID: $IPFS_PID)"
else
    echo "✗ Failed to start IPFS daemon"
    exit 1
fi

echo ""
echo "========================================================"
echo "Starting Flask Web Server..."
echo "========================================================"
echo ""

# Start Flask app
python3 web_app.py

# Cleanup on exit
echo ""
echo "Stopping IPFS daemon..."
kill $IPFS_PID
echo "✓ Shutdown complete"
