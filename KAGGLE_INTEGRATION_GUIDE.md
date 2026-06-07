# Kaggle Dataset Integration Guide

This guide explains how to use the new unified dataset converter to combine your Superstore and E-commerce datasets.

## Step 1: Download Datasets

Download from Kaggle:
1. **Superstore Sales Dataset**
   - URL: https://www.kaggle.com/datasets/laibaanwer/superstore-sales-dataset
   - Extract the CSV file

2. **E-commerce Transactions Dataset**
   - URL: https://www.kaggle.com/datasets/smayanj/e-commerce-transactions-dataset
   - Extract the CSV file

## Step 2: Prepare Files

Create a `raw_data/` folder in your project root and place both CSV files there:

```
PROJECT/
├── raw_data/
│   ├── superstore_sales.csv
│   └── ecommerce_transactions.csv
├── data/
├── scripts/
└── ...
```

## Step 3: Run the Converter

```powershell
cd PROJECT
python scripts/kaggle_data_converter.py
```

## What the Converter Does

### Input Columns Unification

**Superstore Dataset:**
- Order ID → `order_id`
- Product Name → `product_name`
- Category → `category`
- Sales → `price`
- Profit → `profit`
- Quantity → `quantity`
- Region → `region`
- Order Date → `sale_date`
- **Mode added:** `Offline`

**E-commerce Dataset:**
- InvoiceNo → `order_id`
- Description → `product_name`
- StockCode → `product_id` (optional)
- Quantity → `quantity`
- UnitPrice → `price`
- InvoiceDate → `sale_date`
- Country → `region`
- **Category added:** `Electronics` (default)
- **Profit calculated:** price × quantity × 0.30 (adjust as needed)
- **Mode added:** `Online`

### Processing Steps

1. **Load** both CSV files
2. **Standardize** column names and formats
3. **Add missing columns** (Mode, Profit, Category as needed)
4. **Handle missing values** (NULL, empty, invalid entries)
5. **Remove cancelled orders** (negative quantities in e-commerce data)
6. **Combine** using `pd.concat()`
7. **Generate products.csv** from unique product records
8. **Save** clean CSVs to `data/` folder

### Output Files

#### `data/sales.csv`
Combined transaction records with columns:
- `sale_id` - Unique transaction identifier
- `product_name` - Product name
- `quantity` - Units sold
- `mode` - Online or Offline
- `sale_date` - Transaction date

#### `data/products.csv`
Unique product metadata:
- `product_id` - Unique identifier
- `product_name` - Product name
- `category` - Product category
- `avg_price` - Average selling price
- `total_sold` - Total units sold
- `total_profit` - Total profit generated

## Customization

### Change Profit Margin for E-commerce

In `kaggle_data_converter.py`, line ~165:
```python
df['profit'] = (df['price'] * df['quantity']) * 0.30  # Change 0.30 to your margin
```

### Change Default Category

In `kaggle_data_converter.py`, line ~147:
```python
df['category'] = 'Electronics'  # Change to your category
```

### Adjust Column Mappings

Edit the `column_mapping` dictionaries in `standardize_superstore()` and `standardize_ecommerce()` methods to match your exact column names.

## Troubleshooting

### FileNotFoundError
- Ensure raw_data folder exists
- Check file names match exactly (case-sensitive)
- Verify CSV files are in the correct location

### Column Not Found
- Check your CSV column names match the mapping in the converter
- Run `df.columns` to see actual column names in your data

### Missing Values
- The converter automatically handles NULLs and removes incomplete records
- Check the console output for how many rows were removed

## Next Steps

After running the converter:
1. The `data/` folder will have `sales.csv` and `products.csv`
2. Delete old CSV files (if desired)
3. Run your project - it will automatically use the new data

## Manual Column Mapping

If your datasets have different column names, edit the mapping dictionaries:

```python
column_mapping = {
    'Your Column Name': 'standard_name',
    'Another Column': 'standard_name',
}
```

Standard names must be one of:
- `order_id`
- `product_name`
- `category`
- `quantity`
- `price`
- `profit`
- `sale_date`
- `region`
