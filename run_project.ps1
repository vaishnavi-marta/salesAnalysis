# =======================================================================
#  HYBRID SALES & PROFIT ANALYSIS SYSTEM - RUN
#  Class 12 IP Project Launcher
# =======================================================================

Write-Host @"
=======================================================================
 HYBRID SALES & PROFIT ANALYSIS SYSTEM
=======================================================================
"@ -ForegroundColor Cyan

Write-Host "1. Python console menu" -ForegroundColor White
Write-Host "2. HTML sales dashboard" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Choose an interface (1 or 2)"
$scriptPath = if ($choice -eq "1") {
    Join-Path $PSScriptRoot "scripts\main.py"
} elseif ($choice -eq "2") {
    Join-Path $PSScriptRoot "scripts\gui_dashboard.py"
} else {
    Write-Host "Invalid choice. Please select 1 or 2." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

try {
    python $scriptPath
    if ($LASTEXITCODE -ne 0) {
        throw "Application exited with code $LASTEXITCODE"
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to start the application!" -ForegroundColor Red
    Write-Host "Make sure Python and the required packages are installed." -ForegroundColor Yellow
    Write-Host "Run setup.ps1 first if you haven't already." -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"