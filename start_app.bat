@echo off
REM CropScout AI-oT Launcher for Windows
REM This batch file launches the Streamlit app from the correct directory

cd /d "%~dp0"
echo Launching CropScout AI-oT - KrishiMitra Plant Disease Recognition System...
echo.
streamlit run core/main.py
pause
