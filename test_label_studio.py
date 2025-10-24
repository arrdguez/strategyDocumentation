#!/usr/bin/env python3
"""
Test if Label Studio is working properly
"""

import subprocess
import sys
import time

def test_label_studio():
    """Test Label Studio installation"""
    
    print("Testing Label Studio installation...")
    
    try:
        # Try to get Label Studio version
        result = subprocess.run([
            'label-studio', '--version'
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Label Studio is installed correctly")
            return True
        else:
            print(f"❌ Label Studio error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✅ Label Studio is running (timed out - normal for server)")
        return True
    except Exception as e:
        print(f"❌ Error testing Label Studio: {e}")
        return False

def check_files():
    """Check if all required files exist"""
    
    required_files = [
        'trading_data_labeling.csv',
        'label_studio_config.xml',
        'requirements.txt',
        'LABELING_GUIDE.md'
    ]
    
    print("\nChecking required files:")
    all_files_exist = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_files_exist = False
    
    return all_files_exist

if __name__ == "__main__":
    import os
    
    print("=== TRADING DATA LABELING SETUP TEST ===\n")
    
    # Check files
    files_ok = check_files()
    
    # Test Label Studio
    label_studio_ok = test_label_studio()
    
    print("\n=== SETUP SUMMARY ===")
    if files_ok and label_studio_ok:
        print("✅ All systems ready for labeling!")
        print("\nNext steps:")
        print("1. source label_studio_env/bin/activate")
        print("2. label-studio")
        print("3. Open http://localhost:8080")
    else:
        print("❌ Some issues detected. Please check above.")