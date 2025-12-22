#!/usr/bin/env python
"""
🌾 CropScout AI-oT Quick Launcher
Fastest way to start the app!

Usage: python launch.py
"""

import subprocess
import sys
import os
import time

def main():
    print("╔════════════════════════════════════════════════════════╗")
    print("║   🌾 CropScout AI-oT - KrishiMitra  System 🌾         ║")
    print("║        Plant Disease Recognition Platform            ║")
    print("╚════════════════════════════════════════════════════════╝\n")
    
    # Get the directory where this script is
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("📂 Project Directory:", script_dir)
    print("🧠 Model Location: models/disease_cnn.keras")
    print("✅ Your trained model WILL be used!")
    print("\n⏳ Starting Streamlit app from core/main.py...")
    print("⌛ This may take 30-60 seconds on first run...\n")
    
    time.sleep(2)
    
    # Change to script directory
    os.chdir(script_dir)
    
    # Run streamlit with the correct path
    cmd = [sys.executable, "-m", "streamlit", "run", "core/main.py"]
    
    print(f"🚀 Running: {' '.join(cmd)}\n")
    print("=" * 60)
    
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\n\n👋 App stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
