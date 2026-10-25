# QUICK START GUIDE

## Project: Hybrid Sales and Profit Analysis System

---

## 📁 Project Files Overview

```
PROJECT/
│
├── 📋 DOCUMENTATION
│   ├── README.md                  → User guide and feature overview
│   ├── PROJECT_SYNOPSIS.md        → Detailed project description for school
│   ├── SYLLABUS_MAPPING.md        → Class 12 IP syllabus alignment
│   └── QUICK_START_GUIDE.md       → This file
│
├── 🐍 PYTHON MODULES
│   ├── main.py                    → Menu-driven application (entry point)
│   ├── data_processing.py         → Pandas DataFrames, CSV I/O
│   ├── analysis.py                → SQL-like queries (GROUP BY, aggregates)
│   └── visualization.py           → Matplotlib plots (bar, line, histogram)
│
├── 📊 DATA FILES
│   ├── products.csv              → Product master data (5 products)
│   ├── sales.csv                 → Sales transactions (10 records)
│   └── test_export.csv           → Sample export output
│
├── 📈 TESTING & VERIFICATION
│   ├── verify_project.py         → Comprehensive test suite
│   └── requirements.txt          → Dependencies (pandas, matplotlib)
```

---

## ⚡ Quick Setup (2 minutes)

### Option A: Automated Setup (Recommended)

**For Windows Command Prompt:**
```cmd
setup.bat
```

**For Windows PowerShell:**
```powershell
.\setup.ps1
```

The setup script will:
- ✅ Check Python installation (3.8+ required)
- ✅ Install pandas, matplotlib, numpy
- ✅ Verify all project files
- ✅ Test library functionality
- ✅ Run complete project verification

### Option B: Manual Setup

**Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Run Main Application**
```bash
python scripts\main.py
```

**Step 3: Verify Installation**
```bash
python scripts\verify_project.py
```

---

## 🚀 Running the Project

### Choose Your Interface

**Windows PowerShell (Recommended):**
```powershell
.\run_project.ps1
```

Choose the Python console menu or CustomTkinter desktop dashboard.

### Command Line Interface (CLI)
- Traditional text-based menu system
- Perfect for school demonstrations and viva
- Shows all code execution step-by-step

### Direct Python Execution
```bash
python scripts\main.py
```

### CustomTkinter Desktop Dashboard
```bash
python scripts\gui_dashboard.py
```

### Standalone HTML Dashboard
```bash
python scripts\dashboard_server.py
```

This generates `scripts\dashboard.html` from the current CSV data and opens it
in your browser.

---

## 🎯 What You Can Do

### CLI Interface (Command Line)
Perfect for school demonstrations and understanding code execution:

```bash
python scripts\main.py
```

Navigate through menus:
1. **Data Management** - See DataFrames, head/tail, indexing examples
2. **Analysis Queries** - Run SQL-like GROUP BY, SUM, AVG, etc.
3. **Visualization** - Generate horizontally oriented graphs, histograms, and a pie chart; long-label product charts use the available canvas.
4. **Export** - Save analyzed data to CSV

### Complete Test Suite
```bash
python scripts\verify_project.py
```

Shows all 11 syllabus components working:
- ✓ CSV import/export
- ✓ head() and tail()
- ✓ Selection and indexing
- ✓ Boolean filtering
- ✓ Equi-join (merge)
- ✓ Series operations
- ✓ Aggregate functions
- ✓ GROUP BY queries
- ✓ Date functions
- ✓ And more...

### Option 3: Run Individual Modules
```bash
# Load and display data
python -c "from data_processing import *; print(load_products())"

# Run specific analysis
python -c "from analysis import *; profit_by_product()"

# Generate a graph (displays in window)
python -c "from visualization import *; bar_graph_profit_by_product()"
```

---

## 💡 Key Demonstrations for Viva

### Demo 1: Load CSV Files (Pandas)
```python
import pandas as pd
df = pd.read_csv('products.csv')  # Create DataFrame from CSV
print(df.head())                   # Show first rows
```

### Demo 2: Add Profit Column (Mathematical Operation)
```python
df['profit'] = df['quantity'] * (df['selling_price'] - df['cost_price'])
```

The supplied sales CSV already includes `profit`. The application uses that
recorded value and only applies the formula when the profit column is absent
and both price columns are present.

### Demo 3: Boolean Indexing
```python
high_profit = df[df['profit'] > 10000]  # Filter rows
```

### Demo 4: GROUP BY Aggregation (SQL equivalent)
```python
df.groupby('product_name')['profit'].sum()  # Group and sum
```

### Demo 5: Merge DataFrames (Equi-Join)
```python
result = pd.merge(sales_df, products_df, on='product_id')
```

### Demo 6: Date Functions
```python
df['year_month'] = df['sale_date'].dt.to_period('M')
df.groupby('year_month')['profit'].sum()  # Monthly profit, separated by year
```

### Demo 7: Matplotlib Plot
```python
df.groupby('product_name')['profit'].sum().plot(kind='bar')
plt.title('Profit by Product')
plt.xlabel('Product')
plt.ylabel('Profit')
plt.show()
```

---

## 📊 Sample Project Output

### Analysis Results
```
=== PROFIT BY PRODUCT (GROUP BY + SUM) ===
Values are calculated from the supplied CSV data

=== PROFIT BY MODE ===
Online: ₹7,547,396.89
Offline: ₹1,466,618.21

Total profit: ₹9,014,015.10
Transactions: 101,248
```

---

## 📚 Class 12 IP Syllabus Coverage

| Topic | Coverage | Status |
|-------|----------|--------|
| **Pandas** | Series, DataFrames, CSV I/O, indexing, boolean filtering | ✓ Complete |
| **Matplotlib** | Line, bar, histogram, and pie chart | ✓ Complete |
| **SQL Operations** | MAX, MIN, AVG, SUM, COUNT, GROUP BY, JOIN | ✓ Complete |
| **Date Functions** | Year-month extraction | ✓ Complete |
| **Data Visualization** | Four plot types with customization | ✓ Complete |

---

## 🎓 Expected Viva Questions & Quick Answers

### Q: Explain your project's purpose.
**A:** To analyze sales data and provide profit-driven insights for small businesses, comparing online vs offline channels and identifying high-profit products.

### Q: How do you load data from CSV?
**A:** Using `pd.read_csv('filename.csv')` which creates a DataFrame directly from the file.

### Q: What is the profit formula?
**A:** The supplied CSV already contains transaction profit. For another CSV
without a profit column, the program calculates
`quantity * (selling_price - cost_price)` when all required columns are present.

### Q: Explain equi-join in your project.
**A:** We use `pd.merge(sales, products, on='product_id')` to combine sales records with product information using product_id as the matching key.

### Q: How do you filter high-profit products?
**A:** Using boolean indexing: `df[df['profit'] > threshold]` creates a boolean mask and returns matching rows.

### Q: Show all profit by product aggregation.
**A:** `df.groupby('product_name')['profit'].sum()` groups by product and sums profits, equivalent to SQL GROUP BY.

### Q: How are your graphs customized?
**A:** Each graph includes `plt.xlabel()`, `plt.ylabel()`, `plt.title()`, and `plt.legend()` for complete customization.

---

## 🔧 Troubleshooting

### Libraries Not Found
```bash
# Reinstall dependencies
pip install --upgrade pandas matplotlib
```

### CSV Files Not Found
- Make sure you're in the project directory: `cd "c:\...\PROJECT"`
- Verify `products.csv` and `sales.csv` exist

### Plot Not Displaying
- In terminal/IDE, plots may not display. Try in Jupyter or VSCode.
- Use `plt.savefig('output.png')` to save instead.

### Python Version Issue
```bash
# Check version (need 3.7+)
python --version

# Run specific version if available
python3 -c "import pandas; print(pandas.__version__)"
```

---

## 📝 File Descriptions

### main.py
- Entry point for the application
- Menu-driven interface
- Imports from data_processing, analysis, visualization

### data_processing.py
- Load CSV files → DataFrames
- Demonstrate head(), tail(), head/tail
- Selection, indexing, slicing
- Boolean indexing examples
- Merge/join operation
- Series operations
- Export to CSV

### analysis.py
- SQL equivalent queries using Pandas
- GROUP BY aggregations
- Aggregate functions (MAX, MIN, AVG, SUM, COUNT)
- Date function demonstrations
- Smart business insights

### visualization.py
- Bar graphs (profit by product/mode)
- Line plots (monthly trends)
- Histograms (distributions)
- All with customization (labels, titles, legends)

### verify_project.py
- 11 comprehensive tests
- Demonstrates each syllabus requirement
- Shows expected output for each operation
- Perfect for understanding the system

---

## 🎯 Success Checklist

Before submitting, verify:
- [ ] Project runs without errors
- [ ] All CSV files present
- [ ] Dependencies installed (`pip list | grep pandas`)
- [ ] Main menu works (`python main.py`)
- [ ] Verification passes (`python verify_project.py`)
- [ ] Can explain all Pandas operations
- [ ] Can show plots being generated
- [ ] Can discuss SQL equivalents
- [ ] Syllabus mapping document included
- [ ] Project synopsis included

---

## 📞 Getting Help

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'pandas'"
```bash
pip install pandas matplotlib
```

**Issue**: "FileNotFoundError: products.csv"
```bash
# Make sure you're in project directory
cd "c:\Users\HP\Documents\Vaishnavi\class 12 IP\PROJECT"
python main.py
```

**Issue**: Plots not showing in terminal
```bash
# Try in Jupyter Notebook or VSCode with proper environment
python verify_project.py  # Text output will work
```

---

## 🌟 Key Strengths of This Project

1. **Complete Syllabus Coverage**: Every required topic is demonstrated
2. **Real-World Application**: Solves actual business problems
3. **Well-Documented**: Code, docs, and examples included
4. **Modular Design**: Easy to understand and modify
5. **Test Suite Included**: Verification script validates everything
6. **Viva-Ready**: All concepts easily explained with examples
7. **Professional Output**: Formatted results and graphs
8. **Easy to Extend**: Add more features without breaking existing code

---

## 📄 Document Summary

- **README.md**: How to use the system
- **PROJECT_SYNOPSIS.md**: Detailed project overview for school
- **SYLLABUS_MAPPING.md**: Exact syllabus alignment
- **QUICK_START_GUIDE.md**: This file - quick reference

---

**Ready to use!** Choose an option above and start exploring your Class 12 IP project. 🚀