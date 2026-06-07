# 🚀 HYBRID SALES & PROFIT ANALYSIS SYSTEM - SETUP GUIDE

## 📋 Prerequisites

Before running the project, ensure you have:

- **Windows 10/11** (or compatible OS)
- **Python 3.7 or higher** installed
- **Internet connection** (for initial setup)

---

## ⚡ QUICK START (3 Steps)

### Step 1: Download/Extract Project
```
Extract the project folder to your desired location.
Example: C:\Users\YourName\Documents\Projects\
```

### Step 2: Run Setup
```
Double-click: setup.bat
```
This will:
- Check Python installation
- Install required packages (pandas, matplotlib)
- Verify all files are present
- Test the setup

### Step 3: Run the Project
```
Double-click: run_project.bat
```
Or manually: `python main.py`

---

## 📝 DETAILED STEP-BY-STEP GUIDE

### Step 1: Verify Python Installation

1. Open Command Prompt (search for `cmd` in Start menu)
2. Type: `python --version`
3. You should see: `Python 3.x.x` (where x >= 7)

**If Python is not installed:**
- Download from: https://python.org/downloads/
- During installation, check "Add Python to PATH"
- Restart Command Prompt and try again

### Step 2: Navigate to Project Folder

1. Open File Explorer
2. Go to your project folder (e.g., `C:\Users\HP\Documents\Vaishnavi\class 12 IP\PROJECT`)
3. Right-click in empty space → "Open in Terminal" (or use Command Prompt)

### Step 3: Run Setup Script

1. In the project folder, double-click `setup.bat`
2. Wait for the setup to complete
3. You should see:
   ```
   ✓ Python found
   ✓ Packages installed
   ✓ All project files present
   SETUP COMPLETE!
   ```

**If setup fails:**
- Check internet connection
- Try running Command Prompt as Administrator
- Update pip: `python -m pip install --upgrade pip`

### Step 4: Run the Application

**Option A: Using Batch File (Recommended)**
- Double-click `run_project.bat`
- The menu will appear

**Option B: Manual Command**
- Open Command Prompt in project folder
- Type: `python scripts\main.py`
- Press Enter

### Step 5: Navigate the Application

The application will show:

```
HYBRID SALES AND PROFIT ANALYSIS SYSTEM
============================================================

1. Data Management
2. Analysis Queries
3. Data Visualization
4. Export Data
5. Exit

Enter your choice (1-5):
```

- Type a number (1-5) and press Enter
- Explore different menus
- Type `5` to exit

---

## 🧪 VERIFICATION STEPS

### Test 1: Quick Import Test
```bash
python -c "import pandas, matplotlib; print('Libraries OK')"
```

### Test 2: Full Verification
```bash
python verify_project.py
```
Should show "ALL TESTS PASSED"

### Test 3: Individual Module Tests
```bash
# Test data loading
python -c "from data_processing import load_products; print(load_products())"

# Test analysis
python -c "from analysis import profit_by_product; profit_by_product()"
```

---

## 📁 PROJECT STRUCTURE

After setup, your folder should contain:

```
PROJECT/
├── 🐍 Python Files
│   ├── main.py                    # Main application
│   ├── data_processing.py         # Pandas operations
│   ├── analysis.py                # SQL-like queries
│   └── visualization.py           # Matplotlib plots
│
├── 📊 Data Files
│   ├── products.csv              # Product data
│   └── sales.csv                 # Sales transactions
│
├── 🛠️ Setup Files
│   ├── setup.bat                 # Setup script
│   ├── run_project.bat           # Run script
│   └── requirements.txt          # Dependencies
│
├── 📚 Documentation
│   ├── README.md
│   ├── PROJECT_SYNOPSIS.md
│   ├── SYLLABUS_MAPPING.md
│   ├── QUICK_START_GUIDE.md
│   └── SUBMISSION_CHECKLIST.md
│
└── 🧪 Testing
    └── verify_project.py         # Test suite
```

---

## 🔧 TROUBLESHOOTING

### Problem: "Python is not recognized"
**Solution:**
- Reinstall Python and check "Add to PATH"
- Or use full path: `C:\Python311\python.exe main.py`

### Problem: "Module not found"
**Solution:**
```bash
pip install pandas matplotlib
```

### Problem: "Permission denied"
**Solution:**
- Run Command Prompt as Administrator
- Or run setup.bat as Administrator

### Problem: Graphs don't show
**Solution:**
- In terminal, graphs may not display
- Use `plt.savefig('graph.png')` to save instead
- Or run in IDE like VS Code

### Problem: CSV files not found
**Solution:**
- Ensure you're in the correct folder
- Check if files exist: `dir *.csv`

---

## 🎯 WHAT TO EXPECT

### When You Run the Application

1. **Main Menu** appears with 5 options
2. **Data Management** shows DataFrames, head/tail, indexing demos
3. **Analysis** runs SQL-like queries (GROUP BY, SUM, AVG, etc.)
4. **Visualization** displays bar graphs, line plots, histograms
5. **Export** saves analyzed data to CSV

### Sample Output
```
=== PROFIT BY PRODUCT (GROUP BY + SUM) ===
Laptop: ₹100,000
Headphones: ₹8,000
Monitor: ₹6,000
Mouse: ₹4,500
Keyboard: ₹2,500
```

---

## 📞 SUPPORT

If you encounter issues:

1. Check this guide again
2. Run `python verify_project.py` to diagnose
3. Ensure all files are in the same folder
4. Check Python and pip versions

---

## ✅ SUCCESS CHECKLIST

- [ ] Python 3.7+ installed
- [ ] setup.bat ran successfully
- [ ] run_project.bat starts the application
- [ ] Can navigate menus (1-5)
- [ ] Can see data and analysis results
- [ ] verify_project.py shows "ALL TESTS PASSED"

---

**Your Class 12 IP project is now ready to run! 🎉**

For viva preparation, focus on explaining:
- How CSV data is loaded into DataFrames
- Profit calculation formula
- GROUP BY operations
- Graph customization