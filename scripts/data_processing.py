import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / 'data'

# PANDAS: Creating DataFrames from CSV files

def load_products():
    """Load products from CSV file into DataFrame"""
    file_path = DATA_DIR / 'products.csv'
    df_products = pd.read_csv(file_path)
    return df_products


def load_sales():
    """Load sales from CSV file into DataFrame"""
    file_path = DATA_DIR / 'sales.csv'
    df_sales = pd.read_csv(file_path)
    return df_sales


def merge_data():
    """Merge products and sales DataFrames using equi-join (merge)"""
    df_products = load_products()
    df_sales = load_sales()
    # Try to merge on product_id, otherwise fall back to product_name
    if 'product_id' in df_sales.columns and 'product_id' in df_products.columns:
        df_merged = pd.merge(df_sales, df_products, on='product_id', how='left')
    elif 'product_name' in df_sales.columns and 'product_name' in df_products.columns:
        df_merged = pd.merge(df_sales, df_products, on='product_name', how='left')
    else:
        # If no common key, perform a cartesian merge (not ideal) — keep sales only
        df_merged = df_sales.copy()

    # Consolidate product name columns after merge
    if 'product_name_x' in df_merged.columns and 'product_name_y' in df_merged.columns:
        df_merged['product_name'] = df_merged['product_name_x'].fillna(df_merged['product_name_y'])
        df_merged = df_merged.drop(columns=['product_name_x', 'product_name_y'])

    if 'category_x' in df_merged.columns and 'category_y' in df_merged.columns:
        df_merged['category'] = df_merged['category_x'].fillna(df_merged['category_y'])
        df_merged = df_merged.drop(columns=['category_x', 'category_y'])

    return df_merged


def add_profit_column():
    """Add profit column to merged DataFrame"""
    df = merge_data()
    # Ensure numeric types
    if 'quantity' in df.columns:
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce').fillna(0)

    # Determine selling_price from available columns
    if 'selling_price' in df.columns:
        df['selling_price'] = pd.to_numeric(df['selling_price'], errors='coerce')
    elif 'price' in df.columns:
        df['selling_price'] = pd.to_numeric(df['price'], errors='coerce')
    elif 'avg_price' in df.columns:
        df['selling_price'] = pd.to_numeric(df['avg_price'], errors='coerce')
    else:
        df['selling_price'] = 0

    # Determine cost_price; if missing, estimate as 70% of selling_price
    if 'cost_price' in df.columns:
        df['cost_price'] = pd.to_numeric(df['cost_price'], errors='coerce')
    else:
        df['cost_price'] = (df['selling_price'] * 0.70).fillna(0)

    # If profit column already present, coerce numeric, otherwise compute it
    if 'profit' in df.columns:
        df['profit'] = pd.to_numeric(df['profit'], errors='coerce').fillna(0)
    else:
        df['profit'] = df['quantity'] * (df['selling_price'] - df['cost_price'])

    return df


def display_data(df, limit=None):
    """Display DataFrame"""
    print("\nData:")
    print(df.head(limit))


def head_tail_demo(df):
    """Demonstrate head() and tail() functions"""
    print("\n--- HEAD (First 3 rows) ---")
    print(df.head(3))
    print("\n--- TAIL (Last 3 rows) ---")
    print(df.tail(3))


def selection_and_indexing(df):
    """Demonstrate selection, indexing, and slicing"""
    print("\n--- SELECT COLUMNS (ALL RECORDS) ---")
    print(df[['product_name', 'profit']])

    print("\n--- INDEXING (row 0, column 'product_name') ---")
    print(df.loc[0, 'product_name'])

    print("\n--- SLICING (first 10 rows) ---")
    print(df.iloc[0:10])
def boolean_indexing(df):
    """Demonstrate boolean indexing - filter high profit products"""
    high_profit = df[df['profit'] > 5000]
    print("\n--- BOOLEAN INDEXING (profit > 5000) ---")
    print(high_profit[['product_name', 'profit']])
    return high_profit


def rename_columns(df):
    """Demonstrate renaming columns"""
    df_renamed = df.rename(columns={'product_name': 'name', 'profit': 'gain'})
    print("\n--- RENAMED COLUMNS (ALL RECORDS) ---")
    print(df_renamed[['name', 'gain']])
    return df_renamed


def export_to_csv(df, filename):
    """Export DataFrame to CSV file"""
    df.to_csv(filename, index=False)
    print(f"Data exported to {filename}")


def series_operations():
    """Demonstrate Series creation and operations"""
    df = merge_data()
    
    # Series from DataFrame column
    profit_series = df['profit']
    print("\n--- SERIES from column (ALL RECORDS) ---")
    print(profit_series)
    
    # Mathematical operations on Series
    print("\n--- SERIES Mathematical Operations ---")
    print(f"Sum: {profit_series.sum()}")
    print(f"Mean: {profit_series.mean()}")
    print(f"Max: {profit_series.max()}")
    print(f"Min: {profit_series.min()}")
