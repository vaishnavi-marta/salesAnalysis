# =======================================================================
#  HYBRID SALES & PROFIT ANALYSIS SYSTEM - SETUP
#  Class 12 IP Project | Complete Installation Guide
# =======================================================================
# This script will set up the project on a new system.
# Follow the checkpoints and resolve any errors before proceeding.

Write-Host "=======================================================================
 HYBRID SALES & PROFIT ANALYSIS SYSTEM - SETUP
 Class 12 IP Project | Complete Installation Guide
=======================================================================
" -ForegroundColor Cyan

Write-Host "This script will set up the project on a new system."
Write-Host "Follow the checkpoints and resolve any errors before proceeding."
Write-Host ""
Read-Host "Press Enter to start setup"

# =======================================================================
# [CHECKPOINT 1/6] SYSTEM REQUIREMENTS VERIFICATION
# =======================================================================
Write-Host "=======================================================================
[CHECKPOINT 1/6] SYSTEM REQUIREMENTS VERIFICATION
=======================================================================
" -ForegroundColor Yellow

Write-Host "Step 1.1: Checking Windows version..." -ForegroundColor Green
$osInfo = Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion
Write-Host "OK Windows detected: $($osInfo.WindowsProductName) (Version: $($osInfo.WindowsVersion))" -ForegroundColor Green
Write-Host ""

Write-Host "Step 1.2: Checking for PowerShell..." -ForegroundColor Green
$psVersion = $PSVersionTable.PSVersion
Write-Host "OK PowerShell $psVersion available" -ForegroundColor Green
Write-Host ""

Write-Host "Step 1.3: Checking project directory structure..." -ForegroundColor Green
$requiredFolders = @("scripts", "data")
$requiredFiles = @("requirements.txt")

$missingItems = @()

foreach ($folder in $requiredFolders) {
    if (-not (Test-Path $folder)) {
        $missingItems += "Folder: $folder"
    }
}

foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        $missingItems += "File: $file"
    }
}

if ($missingItems.Count -gt 0) {
    Write-Host "ERROR: Missing required items!" -ForegroundColor Red
    Write-Host "Missing:" -ForegroundColor Red
    foreach ($item in $missingItems) {
        Write-Host "  - $item" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "SOLUTION: Ensure all project files are extracted to the same folder." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "OK Project folder structure OK" -ForegroundColor Green
Write-Host ""

# =======================================================================
# [CHECKPOINT 2/6] PYTHON INSTALLATION VERIFICATION
# =======================================================================
Write-Host "=======================================================================
[CHECKPOINT 2/6] PYTHON INSTALLATION VERIFICATION
=======================================================================
" -ForegroundColor Yellow

Write-Host "Step 2.1: Checking Python installation..." -ForegroundColor Green
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "OK Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUTION:" -ForegroundColor Yellow
    Write-Host "1. Download Python from: https://python.org" -ForegroundColor White
    Write-Host "2. During installation, check 'Add Python to PATH'" -ForegroundColor White
    Write-Host "3. Or install via Microsoft Store: winget install Python.Python.3" -ForegroundColor White
    Write-Host "4. Restart PowerShell and run setup again" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 2.2: Checking Python version..." -ForegroundColor Green
$pythonVersionOutput = python --version 2>&1
$versionMatch = $pythonVersionOutput | Select-String -Pattern "Python (\d+)\.(\d+)\.(\d+)"
if ($versionMatch) {
    $majorVersion = [int]$versionMatch.Matches[0].Groups[1].Value
    $minorVersion = [int]$versionMatch.Matches[0].Groups[2].Value

    if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 8)) {
        Write-Host "ERROR: Python 3.8+ required, found Python $majorVersion.$minorVersion" -ForegroundColor Red
        Write-Host "SOLUTION: Install Python 3.8 or higher" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host "OK Python $pythonVersionOutput OK (3.8+ required)" -ForegroundColor Green
} else {
    Write-Host "WARNING: Could not parse Python version, continuing..." -ForegroundColor Yellow
}
Write-Host ""

# =======================================================================
# [CHECKPOINT 3/6] PYTHON PACKAGE INSTALLATION
# =======================================================================
Write-Host "=======================================================================
[CHECKPOINT 3/6] PYTHON PACKAGE INSTALLATION
=======================================================================
" -ForegroundColor Yellow

Write-Host "Step 3.1: Upgrading pip (package installer)..." -ForegroundColor Green
try {
    python -m pip install --upgrade pip 2>&1 | Out-Null
    Write-Host "OK Pip upgrade attempted" -ForegroundColor Green
} catch {
    Write-Host "WARNING: pip upgrade failed, but continuing..." -ForegroundColor Yellow
}
Write-Host ""

Write-Host "Step 3.2: Installing required packages..." -ForegroundColor Green
Write-Host "Installing: pandas, matplotlib, numpy, customtkinter" -ForegroundColor White
try {
    pip install -r requirements.txt 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Package installation failed"
    }
    Write-Host "OK All packages installed successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Package installation failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "SOLUTIONS:" -ForegroundColor Yellow
    Write-Host "1. Check internet connection" -ForegroundColor White
    Write-Host "2. Try: pip install --upgrade pip" -ForegroundColor White
    Write-Host "3. Try: pip install pandas matplotlib numpy --upgrade" -ForegroundColor White
    Write-Host "4. If behind proxy/firewall, configure proxy settings" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# =======================================================================
# [CHECKPOINT 4/6] PROJECT FILES VERIFICATION
# =======================================================================
Write-Host "=======================================================================
[CHECKPOINT 4/6] PROJECT FILES VERIFICATION
=======================================================================
" -ForegroundColor Yellow

Write-Host "Step 4.1: Checking core Python scripts..." -ForegroundColor Green
$requiredScripts = @(
    "scripts\main.py",
    "scripts\data_processing.py",
    "scripts\analysis.py",
    "scripts\visualization.py",
    "scripts\verify_project.py"
)

$missingScripts = @()
foreach ($script in $requiredScripts) {
    if (-not (Test-Path $script)) {
        $missingScripts += $script
    }
}

if ($missingScripts.Count -gt 0) {
    Write-Host "ERROR: Missing Python scripts!" -ForegroundColor Red
    foreach ($script in $missingScripts) {
        Write-Host "  - $script" -ForegroundColor Red
    }
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "OK All Python scripts present" -ForegroundColor Green
Write-Host ""

Write-Host "Step 4.2: Checking data files..." -ForegroundColor Green
$requiredDataFiles = @("data\products.csv", "data\sales.csv")

$missingDataFiles = @()
foreach ($file in $requiredDataFiles) {
    if (-not (Test-Path $file)) {
        $missingDataFiles += $file
    }
}

if ($missingDataFiles.Count -gt 0) {
    Write-Host "ERROR: Missing data files!" -ForegroundColor Red
    foreach ($file in $missingDataFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "SOLUTION: Run conversion script if needed" -ForegroundColor Yellow
    Write-Host "Command: python scripts\convert_kaggle_to_csv.py" -ForegroundColor White
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "OK Data files present" -ForegroundColor Green
Write-Host ""

Write-Host "Step 4.3: Checking batch files..." -ForegroundColor Green
$requiredBatchFiles = @("run_project.bat")

$missingBatchFiles = @()
foreach ($file in $requiredBatchFiles) {
    if (-not (Test-Path $file)) {
        $missingBatchFiles += $file
    }
}

if ($missingBatchFiles.Count -gt 0) {
    Write-Host "ERROR: Missing batch files!" -ForegroundColor Red
    foreach ($file in $missingBatchFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "OK Batch files present" -ForegroundColor Green
Write-Host ""

# =======================================================================
# [CHECKPOINT 5/6] LIBRARY FUNCTIONALITY TEST
# =======================================================================
Write-Host "=======================================================================
[CHECKPOINT 5/6] LIBRARY FUNCTIONALITY TEST
=======================================================================
" -ForegroundColor Yellow

Write-Host "Step 5.1: Testing pandas import..." -ForegroundColor Green
try {
    $pandasVersion = python -c "import pandas as pd; print(pd.__version__)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "pandas import failed"
    }
    Write-Host "OK pandas $pandasVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: pandas not working" -ForegroundColor Red
    Write-Host "SOLUTION: pip install pandas --upgrade" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 5.2: Testing matplotlib import..." -ForegroundColor Green
try {
    $matplotlibVersion = python -c "import matplotlib; print(matplotlib.__version__)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "matplotlib import failed"
    }
    Write-Host "OK matplotlib $matplotlibVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: matplotlib not working" -ForegroundColor Red
    Write-Host "SOLUTION: pip install matplotlib --upgrade" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 5.3: Testing numpy import..." -ForegroundColor Green
try {
    $numpyVersion = python -c "import numpy as np; print(np.__version__)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "numpy import failed"
    }
    Write-Host "OK numpy $numpyVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: numpy not working" -ForegroundColor Red
    Write-Host "SOLUTION: pip install numpy --upgrade" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 5.4: Testing CustomTkinter import..." -ForegroundColor Green
try {
    $customTkVersion = python -c "import customtkinter as ctk; print(ctk.__version__)" 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "CustomTkinter import failed"
    }
    Write-Host "OK CustomTkinter $customTkVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: CustomTkinter not working" -ForegroundColor Red
    Write-Host "SOLUTION: pip install customtkinter --upgrade" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# =======================================================================
# [CHECKPOINT 6/6] FINAL PROJECT VERIFICATION
# =======================================================================
Write-Host "=======================================================================
[CHECKPOINT 6/6] FINAL PROJECT VERIFICATION
=======================================================================
" -ForegroundColor Yellow

Write-Host "Step 6.1: Running project verification..." -ForegroundColor Green
try {
    python scripts\verify_project.py 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Project verification failed"
    }
    Write-Host "OK Project verification passed" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Project verification failed!" -ForegroundColor Red
    Write-Host "SOLUTION: Check error messages above and fix issues" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

# =======================================================================
# SUCCESS MESSAGE
# =======================================================================
Write-Host "=======================================================================
SETUP COMPLETE! PROJECT READY TO RUN
=======================================================================
" -ForegroundColor Green

Write-Host "All checkpoints passed successfully!" -ForegroundColor Green
Write-Host "Project is fully configured and ready to use" -ForegroundColor Green
Write-Host ""

Write-Host "=======================================================================
NEXT STEPS:
=======================================================================
" -ForegroundColor Cyan

Write-Host "1. RUN THE PROJECT:" -ForegroundColor Yellow
Write-Host "   - Double-click: run_project.bat" -ForegroundColor White
Write-Host "   - Or manually: python scripts\main.py" -ForegroundColor White
Write-Host ""

Write-Host "2. VERIFY FUNCTIONALITY:" -ForegroundColor Yellow
Write-Host "   - Run: python scripts\verify_project.py" -ForegroundColor White
Write-Host ""

Write-Host "3. EXPLORE FEATURES:" -ForegroundColor Yellow
Write-Host "   - Sales & profit analysis" -ForegroundColor White
Write-Host "   - Online vs Offline comparisons" -ForegroundColor White
Write-Host "   - Monthly trend analysis" -ForegroundColor White
Write-Host "   - Data export capabilities" -ForegroundColor White
Write-Host "   - Visualization charts" -ForegroundColor White
Write-Host ""

Write-Host "4. CONVERT NEW DATASETS (if needed):" -ForegroundColor Yellow
Write-Host "   - Run: python scripts\convert_kaggle_to_csv.py" -ForegroundColor White
Write-Host "   - Enter path to your Kaggle CSV file" -ForegroundColor White
Write-Host ""

Write-Host "=======================================================================
TROUBLESHOOTING:
=======================================================================
" -ForegroundColor Cyan

Write-Host "If you encounter issues:" -ForegroundColor Yellow
Write-Host "- Run setup.ps1 again" -ForegroundColor White
Write-Host "- Check error messages carefully" -ForegroundColor White
Write-Host "- Ensure all files are in the correct folders" -ForegroundColor White
Write-Host "- Verify internet connection for package installation" -ForegroundColor White
Write-Host "- Check Python PATH if commands fail" -ForegroundColor White
Write-Host ""

Write-Host "For help: Check README.md and SETUP_GUIDE.md" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"