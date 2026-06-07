# Setup Instructions for New Kaggle Datasets

## Step 1: Download the Datasets

Download both datasets from Kaggle:

### Dataset 1: Superstore Sales
- **URL**: https://www.kaggle.com/datasets/laibaanwer/superstore-sales-dataset
- **Download**: Click the download button or use Kaggle CLI
- **Look for**: CSV file containing Order ID, Product Name, Category, Sales, Profit, Quantity, Region, Order Date

### Dataset 2: E-commerce Transactions
- **URL**: https://www.kaggle.com/datasets/smayanj/e-commerce-transactions-dataset
- **Download**: Click the download button or use Kaggle CLI
- **Look for**: CSV file containing InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

## Step 2: Setup Your Project

1. Create a `raw_data/` folder in your project root:
```powershell
mkdir raw_data
```

2. Extract and place the CSV files into this folder:
```
PROJECT/
├── raw_data/
│   ├── superstore_sales.csv        (or whatever the file is named)
│   └── ecommerce_transactions.csv  (or whatever the file is named)
├── data/                           (currently empty - cleaned)
├── scripts/
└── ...
```

## Step 3: Run the Data Converter

Once your CSV files are in `raw_data/`, run:

```powershell
python scripts\kaggle_data_converter.py
```

This will:
- ✓ Standardize all column names
- ✓ Add "Mode" column (Offline for Superstore, Online for E-commerce)
- ✓ Calculate missing profit values
- ✓ Clean and validate the data
- ✓ Generate `data/sales.csv` and `data/products.csv`

## Step 4: Verify the Data

The converter will display a preview with:
- Total rows and columns
- Date range of transactions
- Revenue and profit statistics
- Online vs Offline breakdown
- Top 5 products

## Troubleshooting

**Files not found?**
- Check the exact CSV filenames downloaded from Kaggle
- Edit `main()` function in `scripts/kaggle_data_converter.py` to use your file names

**Column names don't match?**
- The converter has built-in column mapping
- If still issues, edit the `column_mapping` dictionaries in the converter

**Need a fresh start?**
- Delete `raw_data/` folder
- Delete any files in `data/`
- Re-download the datasets
- Start from Step 2

## Notes

- The project is ready to accept any Kaggle dataset once you run the converter
- Your Satoshi font is configured (falls back to Arial if not installed)
- Charts are optimized at 4.5x4.5 inches for the dashboard
