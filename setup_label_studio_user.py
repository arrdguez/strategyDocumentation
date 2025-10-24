#!/usr/bin/env python3
"""
Setup Label Studio with default user credentials
"""

import os
import subprocess
import sys

def setup_label_studio():
    """Setup Label Studio with default user"""
    
    print("Setting up Label Studio user...")
    
    # Stop any running Label Studio instance
    print("Stopping any running Label Studio instances...")
    subprocess.run(['pkill', '-f', 'label-studio'], capture_output=True)
    
    # Remove existing database to start fresh
    db_path = os.path.expanduser('~/.local/share/label-studio')
    if os.path.exists(db_path):
        print(f"Removing existing database at {db_path}")
        subprocess.run(['rm', '-rf', db_path])
    
    # Set environment variables for default user
    env = os.environ.copy()
    env['USERNAME'] = 'trader'
    env['PASSWORD'] = 'trading123'
    
    # Start Label Studio with init flag
    print("Starting Label Studio with default user setup...")
    print("Username: trader")
    print("Password: trading123")
    
    try:
        # Use --no-browser to avoid opening browser automatically
        process = subprocess.Popen([
            'label-studio', 'start', '--no-browser', '--username', 'trader', '--password', 'trading123'
        ], env=env)
        
        print("\n✅ Label Studio started with default credentials!")
        print("\nAccess at: http://localhost:8080")
        print("Username: trader")
        print("Password: trading123")
        print("\nPress Ctrl+C to stop Label Studio")
        
        # Wait for process
        process.wait()
        
    except KeyboardInterrupt:
        print("\nStopping Label Studio...")
        process.terminate()
    except Exception as e:
        print(f"Error: {e}")

def create_simple_start_script():
    """Create a simple startup script"""
    
    script_content = """#!/bin/bash
# Simple Label Studio startup script

source label_studio_env/bin/activate
label-studio start --no-browser --username trader --password trading123
"""
    
    with open('start_labeling.sh', 'w') as f:
        f.write(script_content)
    
    subprocess.run(['chmod', '+x', 'start_labeling.sh'])
    print("✅ Created startup script: ./start_labeling.sh")

if __name__ == "__main__":
    print("=== LABEL STUDIO USER SETUP ===")
    create_simple_start_script()
    print("\nTo start Label Studio with default user:")
    print("./start_labeling.sh")
    print("\nOr manually:")
    print("source label_studio_env/bin/activate")
    print("label-studio start --no-browser --username trader --password trading123")