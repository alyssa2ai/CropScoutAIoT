# CropScout AI-oT Launcher for PowerShell
# This script launches the Streamlit app from the correct directory
# Usage: powershell -ExecutionPolicy Bypass -File start_app.ps1

Write-Host "╔════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   🌾 CropScout AI-oT - KrishiMitra System 🌾          ║" -ForegroundColor Cyan
Write-Host "║        Plant Disease Recognition Platform            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Cyan

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Change to script directory
Set-Location $scriptDir

Write-Host "`n📂 Working Directory: $(Get-Location)" -ForegroundColor Green
Write-Host "🚀 Launching Streamlit app from core/main.py..." -ForegroundColor Green
Write-Host "`n⏳ App is starting... This may take 30-60 seconds on first run" -ForegroundColor Yellow
Write-Host "🌐 Once loaded, open your browser to: http://localhost:8501" -ForegroundColor Yellow
Write-Host "`n" -ForegroundColor White

# Launch Streamlit
streamlit run core/main.py
