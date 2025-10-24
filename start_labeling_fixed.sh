#!/bin/bash
# Fixed Label Studio startup script - NO AUTHENTICATION REQUIRED

echo "=== TRADING DATA LABELING STARTUP (NO LOGIN REQUIRED) ==="
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

# Start Label Studio WITHOUT authentication
echo ""
echo "🚀 Starting Label Studio WITHOUT authentication..."
echo "📊 Access at: http://localhost:8080"
echo "🔓 NO LOGIN REQUIRED - Just click 'Sign Up' to create your account"
echo ""
echo "Steps:"
echo "1. Open http://localhost:8080"
echo "2. Click 'Sign Up'"
echo "3. Create any username/password you want"
echo "4. Start labeling!"
echo ""
echo "Press Ctrl+C to stop Label Studio"
echo ""

# Start Label Studio with signup enabled
LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK=false label-studio start --no-browser