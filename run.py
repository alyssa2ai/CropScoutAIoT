"""
🌾 CropScout AI-oT - KrishiMitra Plant Disease Recognition System

This is the entry point file that runs the app from the root directory.
The actual app code is in: core/main.py

To run:
    streamlit run run.py

Or use the helper scripts:
    - Windows: start_app.bat
    - PowerShell: start_app.ps1
    - Direct: streamlit run core/main.py
"""

# Import the main app from core folder
import os
import sys

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'core'))
sys.path.insert(0, os.path.join(current_dir, 'data'))
sys.path.insert(0, os.path.join(current_dir, 'features'))

# Now import and run the main app
# We use exec with the globals from this file so Streamlit can access everything
with open(os.path.join(current_dir, 'core', 'main.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), globals())
