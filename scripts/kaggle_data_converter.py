"""
Kaggle Dataset Converter for Hybrid Sales Analysis
Combines Superstore and E-commerce datasets with standardized structure
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


class DatasetConverter:
    def __init__(self, superstore_path=None, ecommerce_path=None):
        """
        Initialize the converter with dataset paths
        
        Args:
            superstore_path: Path to superstore sales CSV
            ecommerce_path: Path to e-commerce transactions CSV
        """
        self.superstore_path = superstore_path
        self.ecommerce_path = ecommerce_path
        self.superstore_data = None
        self.ecommerce_data = None
        self.combined_data = None

    def load_datasets(self):
        """Load both datasets from CSV files"""
        print("\n[1/6] Loading datasets...")
        try:
            if self.superstore_path:
                self.superstore_data = pd.read_csv(self.superstore_path)
                print(f"Superstore dataset loaded: {self.superstore_data.shape[0]} rows")
                
            if self.ecommerce_path:
                self.ecommerce_data = pd.read_csv(self.ecommerce_path)
                print(f"E-commerce dataset loaded: {self.ecommerce_data.shape[0]} rows")
        except FileNotFoundError as e:
            print(f"✗ Error loading file: {e}")
            return False
        return True

    def standardize_superstore(self):
        """
        Standardize Superstore dataset to unified structure
        Columns: Order ID, Product Name, Category, Sales, Profit, 
                 Quantity, Region, Order Date
        """
        print("\n[2/6] Standardizing Superstore dataset...")
        
        if self.superstore_data is None:
            print("✗ Superstore data not loaded")
            return None

        df = self.superstore_data.copy()

        # Standardize column names (handle various cases)
        column_mapping = {
            'Order ID': 'order_id',
            'order_id': 'order_id',
            'OrderID': 'order_id',
            'Product Name': 'product_name',
            'product_name': 'product_name',
            'ProductName': 'product_name',
            'Category': 'category',
            'category': 'category',
            'Sales': 'price',
            'sales': 'price',
            'Profit': 'profit',
            'profit': 'profit',
            'Quantity': 'quantity',
            'quantity': 'quantity',
            'Region': 'region',
            'region': 'region',
            'Order Date': 'sale_date',
            'order_date': 'sale_date',
            'OrderDate': 'sale_date',
        }

        df.rename(columns=column_mapping, inplace=True)

        # Select only needed columns
        needed_cols = ['order_id', 'product_name', 'category', 'price', 'profit', 'quantity', 'sale_date', 'region']
        df = df[[col for col in needed_cols if col in df.columns]].copy()

        # Standardize date format
        df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')

        # Add Mode column for Offline
        df['mode'] = 'Offline'

        # Handle missing values
        df = df.dropna(subset=['product_name', 'quantity', 'price']).copy()
        df['profit'] = df['profit'].fillna(0)
        df['category'] = df['category'].fillna('Uncategorized')
        df['region'] = df['region'].fillna('Unknown')

        print(f"Superstore standardized: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

    def standardize_ecommerce(self):
        """
        Standardize E-commerce dataset to unified structure
        Columns: InvoiceNo, StockCode, Description, Quantity, 
                 InvoiceDate, UnitPrice, CustomerID, Country
        """
        print("\n[3/6] Standardizing E-commerce dataset...")
        
        if self.ecommerce_data is None:
            print("✗ E-commerce data not loaded")
            return None

        df = self.ecommerce_data.copy()

        # Standardize column names (handle various cases)
        column_mapping = {
            'InvoiceNo': 'order_id',
            'invoiceno': 'order_id',
            'Invoice No': 'order_id',
            'Transaction_ID': 'order_id',
            'TransactionId': 'order_id',
            'StockCode': 'product_id',
            'stockcode': 'product_id',
            'Stock Code': 'product_id',
            'Description': 'product_name',
            'description': 'product_name',
            'Quantity': 'quantity',
            'quantity': 'quantity',
            'InvoiceDate': 'sale_date',
            'invoicedate': 'sale_date',
            'Invoice Date': 'sale_date',
            'Transaction_Date': 'sale_date',
            'TransactionDate': 'sale_date',
            'Transaction Date': 'sale_date',
            'UnitPrice': 'price',
            'unitprice': 'price',
            'Unit Price': 'price',
            'Purchase_Amount': 'price',
            'PurchaseAmount': 'price',
            'Purchase Amount': 'price',
            'Product_Category': 'product_name',
            'ProductCategory': 'product_name',
            'Product Category': 'product_name',
            'CustomerID': 'customer_id',
            'customerid': 'customer_id',
            'Customer ID': 'customer_id',
            'Country': 'region',
            'country': 'region',
        }

        df.rename(columns=column_mapping, inplace=True)

        # Select and prepare columns
        df = df[[col for col in ['order_id', 'product_name', 'quantity', 'price', 'sale_date', 'region'] 
                 if col in df.columns]].copy()

        # If quantity isn't present, assume 1 per transaction
        if 'quantity' not in df.columns:
            df['quantity'] = 1

        # If product_name isn't present but category-like columns exist, keep as product_name
        if 'product_name' not in df.columns and 'Product_Category' in self.ecommerce_data.columns:
            df['product_name'] = self.ecommerce_data['Product_Category']
        # Add category column (if not present)
        if 'category' not in df.columns:
            df['category'] = 'Electronics'  # Default category for e-commerce

        # Standardize date format
        df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')

        # Calculate Profit (estimate as 30% of price)
        # You can adjust this formula based on your margin assumptions
        df['profit'] = (df['price'] * df['quantity']) * 0.30

        # Add Mode column for Online
        df['mode'] = 'Online'

        # Handle missing values
        df = df.dropna(subset=['product_name', 'quantity', 'price'])
        df['profit'] = df['profit'].fillna(0)
        df['category'] = df['category'].fillna('Electronics')
        df['region'] = df['region'].fillna('Unknown')

        # Remove cancelled orders (negative quantities)
        df = df[df['quantity'] > 0].copy()

        print(f"E-commerce standardized: {df.shape[0]} rows, {df.shape[1]} columns")
        return df

    def combine_datasets(self, superstore_df, ecommerce_df):
        """
        Combine both datasets using pd.concat()
        Ensure consistent column structure
        """
        print("\n[4/6] Combining datasets...")

        # Ensure both dataframes have the same columns
        standard_columns = ['order_id', 'product_name', 'category', 'quantity', 'price', 'profit', 'sale_date', 'mode', 'region']

        # Select and reorder columns for superstore
        superstore_df = superstore_df[['order_id', 'product_name', 'category', 'quantity', 'price', 'profit', 'sale_date', 'mode', 'region']]

        # Select and reorder columns for ecommerce (may need adjustment)
        ecommerce_cols = ['order_id', 'product_name', 'category', 'quantity', 'price', 'profit', 'sale_date', 'mode', 'region']
        ecommerce_df = ecommerce_df[[col for col in ecommerce_cols if col in ecommerce_df.columns]]

        # Concatenate using pd.concat()
        combined = pd.concat([superstore_df, ecommerce_df], ignore_index=True, sort=False)

        # Final data cleaning
        combined = combined.dropna(subset=['product_name', 'quantity'])
        combined['profit'] = combined['profit'].fillna(0)
        combined['category'] = combined['category'].fillna('Uncategorized')
        combined['region'] = combined['region'].fillna('Unknown')

        # Remove duplicates based on order_id and product_name
        combined = combined.drop_duplicates(subset=['order_id', 'product_name'], keep='first')

        # Sort by date
        combined = combined.sort_values('sale_date', ascending=True).reset_index(drop=True)

        # Ensure numeric columns are typed correctly
        combined['price'] = pd.to_numeric(combined['price'], errors='coerce')
        combined['quantity'] = pd.to_numeric(combined['quantity'], errors='coerce').fillna(0)
        combined['profit'] = pd.to_numeric(combined['profit'], errors='coerce').fillna(0)

        print(f"Combined dataset created: {combined.shape[0]} rows, {combined.shape[1]} columns")
        print(f"  - Offline (Superstore): {(combined['mode'] == 'Offline').sum()} records")
        print(f"  - Online (E-commerce): {(combined['mode'] == 'Online').sum()} records")

        return combined

    def generate_products_file(self, combined_df):
        """
        Generate a products.csv file from the combined dataset
        Contains unique products with metadata
        """
        print("\n[5/6] Generating products data...")

        df = combined_df.copy()
        # Ensure numeric columns are properly typed before aggregations
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)
        df['profit'] = pd.to_numeric(df['profit'], errors='coerce').fillna(0)

        products = df.groupby('product_name').agg({
            'category': 'first',
            'price': 'mean',
            'quantity': 'sum',
            'profit': 'sum'
        }).reset_index()

        products = products.rename(columns={
            'price': 'avg_price',
            'quantity': 'total_sold',
            'profit': 'total_profit'
        })

        # Add product_id
        products.insert(0, 'product_id', range(1, len(products) + 1))

        print(f"Generated {len(products)} unique products")
        return products

    def save_datasets(self, output_dir='data'):
        """
        Save combined and products datasets to CSV files
        """
        print("\n[6/6] Saving datasets...")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save combined sales data
        if self.combined_data is not None:
            sales_path = os.path.join(output_dir, 'sales.csv')
            products_df = self.generate_products_file(self.combined_data)
            product_map = products_df.set_index('product_name')['product_id'].to_dict()

            sales_df = self.combined_data[[
                'order_id', 'product_name', 'category', 'quantity', 'price', 'profit', 'mode', 'sale_date', 'region'
            ]].copy()
            sales_df['product_id'] = sales_df['product_name'].map(product_map)
            sales_df.rename(columns={'order_id': 'source_order_id'}, inplace=True)
            sales_df.insert(0, 'sale_id', range(1, len(sales_df) + 1))
            sales_df = sales_df[[
                'sale_id', 'source_order_id', 'product_id', 'product_name', 'category', 'quantity', 'price', 'profit', 'mode', 'sale_date', 'region'
            ]]
            sales_df.to_csv(sales_path, index=False)
            print(f"Saved sales.csv ({len(sales_df)} rows)")

        # Save products data
        products_path = os.path.join(output_dir, 'products.csv')
        products_df.to_csv(products_path, index=False)
        print(f"Saved products.csv ({len(products_df)} rows)")

        return sales_path, products_path

    def preview_data(self):
        """Display preview of combined dataset"""
        print("\n" + "="*70)
        print("COMBINED DATASET PREVIEW")
        print("="*70)

        if self.combined_data is None:
            print("No combined data available")
            return

        # Basic statistics
        print(f"\nShape: {self.combined_data.shape[0]} rows × {self.combined_data.shape[1]} columns")
        print(f"\nDate Range: {self.combined_data['sale_date'].min()} to {self.combined_data['sale_date'].max()}")
        print(f"Total Revenue: {self.combined_data['price'].sum():,.2f}")
        print(f"Total Profit: {self.combined_data['profit'].sum():,.2f}")
        print(f"Total Quantity Sold: {self.combined_data['quantity'].sum():,.0f}")

        # Mode breakdown
        print(f"\nSales Mode Breakdown:")
        mode_stats = self.combined_data.groupby('mode').agg({
            'profit': 'sum',
            'order_id': 'count',
            'quantity': 'sum'
        }).rename(columns={'order_id': 'transactions'})
        print(mode_stats)

        # Top products
        print(f"\nTop 5 Products by Profit:")
        top_products = self.combined_data.groupby('product_name')['profit'].sum().nlargest(5)
        for i, (product, profit) in enumerate(top_products.items(), 1):
            print(f"  {i}. {product}: {profit:,.2f}")

        # Data preview
        print(f"\nFirst 5 rows:")
        print(self.combined_data.head(5).to_string())

        print("\n" + "="*70)

    def process(self):
        """
        Main processing pipeline:
        1. Load datasets
        2. Standardize both
        3. Combine
        4. Save
        5. Preview
        """
        print("\n" + "="*70)
        print("HYBRID SALES DATASET CONVERTER")
        print("="*70)

        # Load
        if not self.load_datasets():
            return False

        # Standardize
        superstore_df = self.standardize_superstore()
        ecommerce_df = self.standardize_ecommerce()

        if superstore_df is None or ecommerce_df is None:
            print("✗ Failed to standardize datasets")
            return False

        # Combine
        self.combined_data = self.combine_datasets(superstore_df, ecommerce_df)

        # Save
        self.save_datasets()

        # Preview
        self.preview_data()

        print("\nProcess completed successfully!")
        return True


def main():
    """
    Example usage:
    
    1. Download datasets from Kaggle:
       - https://www.kaggle.com/datasets/laibaanwer/superstore-sales-dataset
       - https://www.kaggle.com/datasets/smayanj/e-commerce-transactions-dataset
    
    2. Place CSV files in a directory (e.g., 'raw_data/')
    
    3. Run this script with the paths to your CSV files
    """
    
    # Paths to your Kaggle datasets
    superstore_file = "raw_data/superstore_sales.csv"  # Adjust to your file path
    ecommerce_file = "raw_data/ecommerce_transactions.csv"  # Adjust to your file path

    # Create converter instance
    converter = DatasetConverter(
        superstore_path=superstore_file,
        ecommerce_path=ecommerce_file
    )

    # Process datasets
    success = converter.process()

    if success:
        print("\nYour unified dataset is ready in the 'data/' folder!")
        print("Files created:")
        print("  - sales.csv (transaction records)")
        print("  - products.csv (product metadata)")
    else:
        print("\nFailed to process datasets. Check file paths and formats.")


if __name__ == '__main__':
    main()
