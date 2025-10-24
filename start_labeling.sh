#!/bin/bash
# Simple Label Studio startup script for trading data labeling

echo "=== TRADING DATA LABELING STARTUP ==="
echo ""

# Check if virtual environment exists
if [ ! -d "label_studio_env" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source label_studio_env/bin/activate

# Stop any running instances
echo "Stopping any running Label Studio instances..."
pkill -f label-studio || true

# Remove existing database to start fresh
echo "Cleaning previous setup..."
rm -rf ~/.local/share/label-studio

# Start Label Studio with default credentials
echo ""
echo "🚀 Starting Label Studio..."
echo "📊 Access at: http://localhost:8080"
echo "👤 Username: trader"
echo "🔑 Password: trading123"
echo ""
echo "Press Ctrl+C to stop Label Studio"
echo ""

# Start Label Studio
label-studio start --no-browser --username trader --password trading123