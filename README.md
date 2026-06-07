# Hybrid Sales and Profit Analysis System for Small Businesses

**Class 12 IP Project - CBSE Aligned**

A comprehensive system that analyzes sales data and provides profit-driven business insights using Pandas, Matplotlib, and CSV data management.

---

## Core Business Logic

The system helps small business owners understand:
- **Product Performance**: Which products generate the most profit?
- **Sales Channel Analysis**: Online vs Offline profitability
- **Monthly Trends**: How profit changes over time
- **Smart Recommendations**: Data-driven business decisions

**Profit Formula**: `Profit = Quantity × (Selling Price - Cost Price)`

---

## Syllabus Coverage

### Pandas (Data Structures & Operations)
- **Series & DataFrames**: Creation from CSV files
- **head() & tail()**: View first/last rows
- **Selection & Indexing**: Using labels and boolean filtering
- **Column Operations**: Add, rename, and manipulate columns
- **Merging**: Equi-join on product_id (SQL-like join)
- **GroupBy**: Simulate SQL GROUP BY operations
- **Import/Export**: Read from and save to CSV files

### Matplotlib (Data Visualization)
- **Bar Graphs**: Product profits, Online vs Offline comparison
- **Line Plots**: Monthly profit trends
- **Histograms**: Distribution of quantities and profits
- **Customization**: Labels, titles, legends, grid

### SQL-like Operations (using Pandas)
- **Aggregate Functions**: SUM(), AVG(), MAX(), MIN(), COUNT()
- **GROUP BY**: Product, mode, month, multiple grouping
- **Mathematical**: Profit calculations
- **Date Functions**: Extract month, month name from dates

---

## Project Structure

```
HYBRID-SALES-ANALYSIS/
├── data/                      # CSV data files for products and sales
│   ├── products.csv
│   └── sales.csv
├── scripts/                   # Python scripts for application logic
│   ├── main.py               # CLI menu-driven application
│   ├── gui_dashboard.py      # GUI dashboard with visual interface
│   ├── data_processing.py    # Pandas DataFrames and CSV operations
│   ├── analysis.py           # SQL-like queries and aggregations
│   ├── visualization.py      # Matplotlib charts and plots
│   └── verify_project.py     # Comprehensive test suite
├── requirements.txt           # Dependencies: pandas, matplotlib, numpy
├── run_project.ps1           # PowerShell launcher (CLI/GUI choice)
├── setup.ps1                 # PowerShell setup script
├── README.md                 # This file
└── SETUP_GUIDE.md            # Detailed step-by-step instructions
```

---

## Requirements

- matplotlib

**Install dependencies**:
```bash
pip install -r requirements.txt
```

---

## How to Run

### Choose Your Interface

**Recommended: Use the launcher script**
```powershell
.\run_project.ps1
```

If you want to launch it from Python instead, use the new wrapper:
```bash
python run_project.py
```

This gives you two options:
1. **Command Line Interface (CLI)** - Traditional menu system
2. **Graphical User Interface (GUI)** - Modern dashboard with buttons

### Direct Commands

**CLI Version (Text-based menus):**
```bash
python scripts/main.py
```

**GUI Version (Visual dashboard):**
```bash
python scripts/gui_dashboard.py
```

**Batch file (Windows only):**
```cmd
run_project.bat
```

### What Each Interface Offers

**CLI Interface:**
- Perfect for school demonstrations and viva
- Shows all code execution step-by-step
- Traditional menu navigation

**GUI Interface:**
- Modern dashboard with visual buttons
- Embedded charts and graphs
- User-friendly for presentations
- Instant results with one click

Both interfaces provide access to:
1. **Data Management** - Explore DataFrames, demonstrate Pandas operations
2. **Analysis** - Run SQL-like queries (GROUP BY, SUM, AVG, MAX, MIN)
3. **Visualization** - Generate Matplotlib plots
4. **Export** - Save analyzed data to CSV

---

## Key Features Demonstrated

### Pandas
- Load CSV files → DataFrames
- head(3), tail(3) - View data boundaries
- Selection by column: `df[['column1', 'column2']]`
- Indexing: `df.loc[0, 'column_name']`
- Slicing: `df.iloc[0:3]`
- Boolean indexing: `df[df['profit'] > 5000]`
- Column renaming: `df.rename(columns={...})`
- GroupBy aggregation: `df.groupby('product').sum()`
- Series operations: Math on single columns

### Matplotlib
- **Bar Graph**: Product vs Profit
- **Bar Graph**: Online vs Offline comparison
- **Line Plot**: Monthly profit trend
- **Histogram**: Quantity distribution
- **Histogram**: Profit distribution
- **Customization**: All graphs include labels, titles, legends

### Analysis Queries
- Profit by Product (GROUP BY + SUM)
- Profit by Mode (GROUP BY + SUM)
- Monthly Profit Trend (GROUP BY MONTH)
- Max/Min Profit Products
- Average & Total Profit
- Count of transactions
- Multiple GROUP BY scenarios

---

## Data Files

### products.csv
```
product_id,product_name,cost_price,selling_price
1,Laptop,50000,60000
2,Mouse,500,800
...
```

### sales.csv
```
sale_id,product_id,quantity,mode,sale_date
1,1,5,Online,2025-01-15
2,2,10,Offline,2025-01-20
...
```

---

## Sample Output

```
=== PROFIT BY PRODUCT (GROUP BY + SUM) ===
Laptop: ₹90000.00
Monitor: ₹18000.00
Mouse: ₹4000.00
...

=== SMART BUSINESS INSIGHTS ===
► Laptop contributes 81.8% of total profit (₹90000.00)
► Online sales are more profitable (₹87000.00 vs ₹23000.00)
► Average profit per transaction: ₹10000.00
```

---

## Viva Questions & Answers

**Q1: What is the profit formula used in your system?**
- A: Profit = Quantity × (Selling Price - Cost Price)

**Q2: Explain how your project uses Pandas.**
- A: We load product and sales data from CSV files into DataFrames, use head()/tail() to view data, perform merges (equi-join) on product_id, and use groupby() to aggregate data (simulating SQL GROUP BY).

**Q3: How do you handle online vs offline sales separately?**
- A: The sales.csv has a 'mode' column (Online/Offline). Using groupby('mode'), we calculate separate profit totals for each channel.

**Q4: Which Matplotlib plots did you use and why?**
- A: Bar graphs show product/mode profits (easy comparison), line plots show monthly trends (time series), and histograms show distribution of quantities/profits.

**Q5: How is your system different from a simple spreadsheet?**
- A: Our system automates analysis through Python, calculates complex aggregations instantly, generates visualizations automatically, and can handle larger datasets efficiently.

**Q6: Explain the purpose of your boolean indexing.**
- A: Boolean indexing filters data (e.g., df[df['profit'] > 5000]) to identify high-profit transactions without manual sorting.

**Q7: How do you export analyzed data?**
- A: We use df.to_csv() to export the merged DataFrame with calculated profit to a new CSV file for further use.

---

## Insights Generated

The system provides automated business recommendations:
- "Online sales are more profitable than offline"
- "Product X contributes 40% of total profit"
- "Sales peak in May"
- "Consider reviewing strategy for low-profit products"

---

## Testing

Sample data is pre-loaded in CSV files. Simply run the program and navigate through menus to see:
- DataFrames loaded and manipulated
- Pandas operations executed
- SQL-like queries running
- Matplotlib visualizations displayed
- Data exported to CSV