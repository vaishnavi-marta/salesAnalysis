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

The supplied sales CSV already records profit. If a different input file lacks
that column, profit is calculated as
`Quantity × (Selling Price - Cost Price)` only when all required values exist.

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
- **Pie Chart**: Profit contribution by sales mode
- **Customization**: Labels, titles, legends, grid

### SQL-like Operations (using Pandas)
- **Aggregate Functions**: SUM(), AVG(), MAX(), MIN(), COUNT()
- **GROUP BY**: Product, mode, year-month, multiple grouping
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
│   ├── gui_dashboard.py      # HTML dashboard launcher
│   ├── dashboard_server.py   # Builds a standalone dashboard from CSV data
│   ├── dashboard.html        # Generated browser dashboard
│   ├── data_processing.py    # Pandas DataFrames and CSV operations
│   ├── analysis.py           # SQL-like queries and aggregations
│   ├── visualization.py      # Matplotlib charts and plots
│   └── verify_project.py     # Comprehensive test suite
├── requirements.txt           # Dependencies: pandas, matplotlib, numpy
├── run_project.ps1           # PowerShell command-line launcher
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

Choose either the Python console menu or the HTML dashboard.

### Direct Commands

**CLI Version (Text-based menus):**
```bash
python scripts/main.py
```

**HTML Dashboard (opens in your browser):**
```bash
python scripts/gui_dashboard.py
```

This creates or refreshes `scripts/dashboard.html` from the current CSV files.
You can also reopen that HTML file directly later. The page is self-contained
and does not use a JSON API.

**Batch file (Windows only):**
```cmd
run_project.bat
```

### What Each Interface Offers

**CLI Interface:**
- Perfect for school demonstrations and viva
- Shows all code execution step-by-step
- Traditional menu navigation

The console menu provides access to:
1. **Data Management** - Explore DataFrames, demonstrate Pandas operations
2. **Analysis** - Run SQL-like queries (GROUP BY, SUM, AVG, MAX, MIN)
3. **Visualization** - Open Matplotlib charts, including a pie chart
4. **Export** - Save analyzed data to CSV

The HTML dashboard shows summary statistics, product and sales-mode charts,
year-month trends, profit distribution, and a searchable transaction sample.

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
- **Pie Chart**: Profit contribution by sales mode
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
product_id,product_name,category,avg_price,total_sold,total_profit
1,"""While you Were Out"" Message Book, One Form per Page",Office Supplies,8.33,8,10.39
2,"#10 Gummed Flap White Envelopes, 100/Box",Office Supplies,10.50,11,16.77
```

### sales.csv
```
sale_id,source_order_id,product_id,product_name,category,quantity,price,profit,mode,sale_date,region
1,AG-2011-2040,3421,"Tenex Lockers, Blue",Office Supplies,2,408.00,106.14,Offline,2011-01-01,Africa
2,IN-2011-47883,169,"Acme Trimmer, High Speed",Office Supplies,3,120.00,36.04,Offline,2011-01-01,Oceania
```

The supplied files contain 3,796 product rows and 101,248 sales transactions.
The transaction file already includes a `profit` value; the program uses that
source value and does not invent a cost price. If a different input file has no
profit column, a profit calculation requires quantity, selling price, and cost
price columns.

---

## Sample Output

```
=== TOTAL PROFIT ===
₹9014015.10

Online profit: ₹7547396.89
Offline profit: ₹1466618.21
Transactions: 101248
```

---

## Viva Questions & Answers

**Q1: How does the system get profit?**
- A: It uses the `profit` column in the provided sales CSV. For another dataset
  without that column, the program can calculate profit only when quantity,
  selling price, and cost price are available.

**Q2: Explain how your project uses Pandas.**
- A: We load product and sales data from CSV files into DataFrames, use head()/tail() to view data, perform merges (equi-join) on product_id, and use groupby() to aggregate data (simulating SQL GROUP BY).

**Q3: How do you handle online vs offline sales separately?**
- A: The sales.csv has a 'mode' column (Online/Offline). Using groupby('mode'), we calculate separate profit totals for each channel.

**Q4: Which Matplotlib plots did you use and why?**
- A: Bar graphs compare product and sales-mode profits, a line plot shows
  year-month trends, histograms show quantity/profit distributions, and a pie
  chart compares profit shares by sales mode.

**Q5: How is your system different from a simple spreadsheet?**
- A: Our system automates analysis through Python, calculates complex aggregations instantly, generates visualizations automatically, and can handle larger datasets efficiently.

**Q6: Explain the purpose of your boolean indexing.**
- A: Boolean indexing filters data (e.g., df[df['profit'] > 5000]) to identify high-profit transactions without manual sorting.

**Q7: How do you export analyzed data?**
- A: We use `df.to_csv()` to save the processed sales DataFrame as a new CSV file.

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