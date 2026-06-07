# =======================================================================
#  HYBRID SALES & PROFIT ANALYSIS SYSTEM - RUN
#  Class 12 IP Project Launcher
# =======================================================================

Write-Host @"
=======================================================================
 HYBRID SALES & PROFIT ANALYSIS SYSTEM
=======================================================================
"@ -ForegroundColor Cyan

Write-Host "Choose your interface:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Command Line Interface (CLI) - Traditional menu system" -ForegroundColor White
Write-Host "2. Graphical User Interface (GUI) - Modern dashboard" -ForegroundColor White
Write-Host ""
$choice = Read-Host "Enter your choice (1 or 2)"

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "Starting Command Line Interface..." -ForegroundColor Green
    Write-Host ""

    try {
        python scripts\main.py
        Write-Host ""
        Write-Host "CLI Application closed successfully." -ForegroundColor Green
    } catch {
        Write-Host ""
        Write-Host "ERROR: Failed to start CLI application!" -ForegroundColor Red
        Write-Host "Make sure Python is installed and setup.ps1 has been run." -ForegroundColor Yellow
    }
} elseif ($choice -eq "2") {
    Write-Host ""
    Write-Host "Starting Graphical User Interface..." -ForegroundColor Green
    Write-Host ""

    try {
        python scripts\gui_dashboard.py
        Write-Host ""
        Write-Host "GUI Application closed successfully." -ForegroundColor Green
    } catch {
        Write-Host ""
        Write-Host "ERROR: Failed to start GUI application!" -ForegroundColor Red
        Write-Host "Make sure Python and required packages are installed." -ForegroundColor Yellow
        Write-Host "Run setup.ps1 first if you haven't already." -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "Invalid choice. Please run the script again and select 1 or 2." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"