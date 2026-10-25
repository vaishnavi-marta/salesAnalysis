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
    if 'product_id' in df_sales.columns and 'product_id' in df_products.columns:
        df_merged = pd.merge(df_sales, df_products, on='product_id', how='left')
    elif 'product_name' in df_sales.columns and 'product_name' in df_products.columns:
        df_merged = pd.merge(df_sales, df_products, on='product_name', how='left')
    else:
        raise ValueError(
            "Cannot merge sales and products: no shared product_id or product_name column."
        )

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
    if 'quantity' in df.columns:
        quantity = pd.to_numeric(df['quantity'], errors='coerce')
        if (df['quantity'].notna() & quantity.isna()).any():
            raise ValueError("The sales data contains non-numeric quantity values.")
        df['quantity'] = quantity

    price_columns = [
        column for column in ('selling_price', 'price', 'avg_price')
        if column in df.columns
    ]
    if price_columns:
        selling_price = pd.Series(float('nan'), index=df.index)
        for column in price_columns:
            price = pd.to_numeric(df[column], errors='coerce')
            if (df[column].notna() & price.isna()).any():
                raise ValueError(f"The sales data contains non-numeric {column} values.")
            selling_price = selling_price.fillna(price)
        df['selling_price'] = selling_price

    if 'profit' in df.columns:
        profit = pd.to_numeric(df['profit'], errors='coerce')
        if (df['profit'].notna() & profit.isna()).any() or profit.isna().any():
            raise ValueError("The sales data contains missing or non-numeric profit values.")
        df['profit'] = profit
    else:
        required_columns = ('quantity', 'selling_price', 'cost_price')
        missing_columns = [column for column in required_columns if column not in df.columns]
        if missing_columns:
            raise ValueError(
                "Cannot calculate profit; missing required columns: "
                + ", ".join(missing_columns)
            )
        if df[list(required_columns)].isna().any().any():
            raise ValueError(
                "Cannot calculate profit because quantity, selling price, "
                "or cost price contains missing values."
            )
        for column in ('selling_price', 'cost_price'):
            df[column] = pd.to_numeric(df[column], errors='coerce')
        if df[list(required_columns)].isna().any().any():
            raise ValueError(
                "Cannot calculate profit because quantity, selling price, "
                "or cost price contains non-numeric values."
            )
        df['profit'] = df['quantity'] * (df['selling_price'] - df['cost_price'])

    return df


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
    df = add_profit_column()
    
    profit_series = df['profit']
    print("\n--- SERIES from column (first 10 records) ---")
    print(profit_series.head(10))
    
    # Mathematical operations on Series
    print("\n--- SERIES Mathematical Operations ---")
    print(f"Sum: {profit_series.sum()}")
    print(f"Mean: {profit_series.mean()}")
    print(f"Max: {profit_series.max()}")
    print(f"Min: {profit_series.min()}")
