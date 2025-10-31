# PCOS Predictor - Create Shareable ZIP
# This script prepares your project for sharing by:
# 1. Removing unnecessary large folders
# 2. Creating a clean ZIP file
# 3. Showing what was included

Write-Host "📦 PCOS Predictor - ZIP Creator" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Get the current directory (should be project root)
$projectRoot = Get-Location
$projectName = "PCOS-rp"
$zipName = "PCOS-Predictor-v1.0.zip"

Write-Host "Project Location: $projectRoot" -ForegroundColor Yellow
Write-Host ""

# Ask for confirmation
Write-Host "⚠️  This will:" -ForegroundColor Yellow
Write-Host "   - Remove backend/venv/ (if exists)" -ForegroundColor White
Write-Host "   - Remove backend/__pycache__/ (if exists)" -ForegroundColor White
Write-Host "   - Remove frontend/node_modules/ (if exists)" -ForegroundColor White
Write-Host "   - Remove backend/.env (if exists)" -ForegroundColor White
Write-Host "   - Create $zipName in parent folder" -ForegroundColor White
Write-Host ""

$confirmation = Read-Host "Continue? (y/n)"
if ($confirmation -ne 'y') {
    Write-Host "Cancelled." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "🧹 Cleaning up unnecessary files..." -ForegroundColor Cyan

# Track what we're removing
$totalSize = 0

# Remove backend venv
if (Test-Path "backend\venv") {
    $size = (Get-ChildItem "backend\venv" -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB
    $totalSize += $size
    Write-Host "  Removing backend/venv/ ($([math]::Round($size, 2)) MB)..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "backend\venv" -ErrorAction SilentlyContinue
}

# Remove backend __pycache__
if (Test-Path "backend\__pycache__") {
    Write-Host "  Removing backend/__pycache__/..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "backend\__pycache__" -ErrorAction SilentlyContinue
}

# Remove frontend node_modules
if (Test-Path "frontend\node_modules") {
    $size = (Get-ChildItem "frontend\node_modules" -Recurse -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum).Sum / 1MB
    $totalSize += $size
    Write-Host "  Removing frontend/node_modules/ ($([math]::Round($size, 2)) MB)..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "frontend\node_modules" -ErrorAction SilentlyContinue
}

# Remove frontend build
if (Test-Path "frontend\build") {
    Write-Host "  Removing frontend/build/..." -ForegroundColor Gray
    Remove-Item -Recurse -Force "frontend\build" -ErrorAction SilentlyContinue
}

# Backup and remove .env
if (Test-Path "backend\.env") {
    Write-Host "  Backing up backend/.env to backend/.env.backup..." -ForegroundColor Gray
    Copy-Item "backend\.env" "backend\.env.backup" -Force
    Remove-Item "backend\.env" -Force
    Write-Host "  ⚠️  Your .env has been backed up to .env.backup" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ Cleaned up $([math]::Round($totalSize, 2)) MB" -ForegroundColor Green
Write-Host ""

# Create the ZIP
Write-Host "📦 Creating ZIP file..." -ForegroundColor Cyan

$parentFolder = Split-Path $projectRoot -Parent
$zipPath = Join-Path $parentFolder $zipName

# Remove old ZIP if exists
if (Test-Path $zipPath) {
    Write-Host "  Removing old ZIP file..." -ForegroundColor Gray
    Remove-Item $zipPath -Force
}

# Create new ZIP
try {
    Write-Host "  Compressing files (this may take a minute)..." -ForegroundColor Gray
    Compress-Archive -Path "$projectRoot\*" -DestinationPath $zipPath -CompressionLevel Optimal -Force
    
    $zipSize = (Get-Item $zipPath).Length / 1MB
    
    Write-Host ""
    Write-Host "================================" -ForegroundColor Green
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "ZIP created: $zipPath" -ForegroundColor White
    Write-Host "ZIP size: $([math]::Round($zipSize, 2)) MB" -ForegroundColor White
    Write-Host ""
    
    # Show what's included
    Write-Host "📋 What's included:" -ForegroundColor Cyan
    Write-Host "  ✅ backend/ (Python files, ML models)" -ForegroundColor Green
    Write-Host "  ✅ frontend/ (React source files)" -ForegroundColor Green
    Write-Host "  ✅ dataset/ (CSV data)" -ForegroundColor Green
    Write-Host "  ✅ Documentation (README, guides)" -ForegroundColor Green
    Write-Host ""
    Write-Host "  ❌ backend/venv/ (excluded)" -ForegroundColor Red
    Write-Host "  ❌ frontend/node_modules/ (excluded)" -ForegroundColor Red
    Write-Host "  ❌ backend/.env (excluded)" -ForegroundColor Red
    Write-Host ""
    
    # Next steps
    Write-Host "📤 Next Steps:" -ForegroundColor Cyan
    Write-Host "  1. Share the ZIP file ($zipName)" -ForegroundColor White
    Write-Host "  2. Recipient should read README.md for setup" -ForegroundColor White
    Write-Host "  3. They'll need to run: setup.ps1 (Windows)" -ForegroundColor White
    Write-Host "  4. Or follow manual setup in SETUP_CHECKLIST.md" -ForegroundColor White
    Write-Host ""
    
    # Restore .env
    if (Test-Path "backend\.env.backup") {
        Write-Host "🔄 Restoring your .env file..." -ForegroundColor Yellow
        Copy-Item "backend\.env.backup" "backend\.env" -Force
        Write-Host "✅ Your .env has been restored" -ForegroundColor Green
        Write-Host ""
    }
    
    Write-Host "All done! 🎉" -ForegroundColor Green
    
    # Ask if they want to open the folder
    $open = Read-Host "Open containing folder? (y/n)"
    if ($open -eq 'y') {
        explorer.exe $parentFolder
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Error creating ZIP: $_" -ForegroundColor Red
    Write-Host ""
    
    # Restore .env on error
    if (Test-Path "backend\.env.backup") {
        Copy-Item "backend\.env.backup" "backend\.env" -Force
        Write-Host "✅ Your .env has been restored" -ForegroundColor Green
    }
}
