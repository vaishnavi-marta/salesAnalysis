#!/usr/bin/env python3
"""
Project Verification Script
Demonstrates all Class 12 IP Syllabus Components
"""

import pandas as pd

print("\n" + "="*70)
print("HYBRID SALES & PROFIT ANALYSIS SYSTEM - PROJECT VERIFICATION")
print("="*70)

# Test 1: Pandas - Load CSV and create DataFrame
print("\n[TEST 1] PANDAS - Loading CSV Files into DataFrames")
print("-" * 70)
import data_processing
df_products = data_processing.load_products()
df_sales = data_processing.load_sales()
print("✓ Products DataFrame created from CSV:")
print(df_products.head(2))
print("\n✓ Sales DataFrame created from CSV:")
print(df_sales.head(2))

# Test 2: Pandas - Head and Tail
print("\n[TEST 2] PANDAS - head() and tail() Functions")
print("-" * 70)
print("First 3 products (head):")
print(df_products.head(3))
print("\nLast 2 products (tail):")
print(df_products.tail(2))

# Test 3: Pandas - Selection and Indexing
print("\n[TEST 3] PANDAS - Selection, Indexing, Slicing")
print("-" * 70)
product_price_column = 'selling_price' if 'selling_price' in df_products.columns else 'avg_price'
print(f"Column selection (product_name, {product_price_column}):")
print(df_products[['product_name', product_price_column]])
print("\nIndexing - Location [0, 'product_name']:", df_products.loc[0, 'product_name'])
print("Slicing - Rows 0-2:")
print(df_products.iloc[0:3])

# Test 4: Pandas - Boolean Indexing
print("\n[TEST 4] PANDAS - Boolean Indexing")
print("-" * 70)
df_full = data_processing.add_profit_column()
price_threshold = df_full['selling_price'].median()
expensive_products = df_full[df_full['selling_price'] > price_threshold]
print(f"Products with selling_price above the median (₹{price_threshold:.2f}):")
print(expensive_products[['product_name', 'selling_price']])

# Test 5: Pandas - Merge/Join
print("\n[TEST 5] PANDAS - Equi-Join (Merge on product_id)")
print("-" * 70)
df_merged = data_processing.merge_data()
print("Merged Data (Sales + Products):")
merge_columns = [
    column for column in
    ('product_name', 'quantity', 'mode', 'price', 'avg_price', 'profit')
    if column in df_merged.columns
]
print(df_merged[merge_columns].head(3))

# Test 6: Pandas - Add Column (Profit Calculation)
print("\n[TEST 6] PANDAS - Add Column Operations")
print("-" * 70)
df_with_profit = data_processing.add_profit_column()
print("With Profit Column (Mathematical Operation):")
print(df_with_profit[['product_name', 'quantity', 'profit']].head(4))

# Test 7: Pandas - Series Operations
print("\n[TEST 7] PANDAS - Series Operations (Math Functions)")
print("-" * 70)
profit_series = df_with_profit['profit']
print(f"Series - Sum (SUM): ₹{profit_series.sum()}")
print(f"Series - Mean (AVG): ₹{profit_series.mean():.2f}")
print(f"Series - Max: ₹{profit_series.max()}")
print(f"Series - Min: ₹{profit_series.min()}")

# Test 8: SQL Aggregate Functions
print("\n[TEST 8] SQL-like AGGREGATE Functions (using Pandas)")
print("-" * 70)
print(f"SUM(profit): ₹{df_with_profit['profit'].sum()}")
print(f"AVG(profit): ₹{df_with_profit['profit'].mean():.2f}")
print(f"MAX(profit): ₹{df_with_profit['profit'].max()}")
print(f"MIN(profit): ₹{df_with_profit['profit'].min()}")
print(f"COUNT(*): {df_with_profit.shape[0]}")

# Test 9: GROUP BY Operations
print("\n[TEST 9] GROUP BY Aggregation (SQL equivalent)")
print("-" * 70)
print("GROUP BY product_name, SUM(profit):")
profit_by_product = df_with_profit.groupby('product_name')['profit'].sum()
print(profit_by_product)

print("\nGROUP BY mode, SUM(profit), COUNT(*):")
mode_stats = df_with_profit.groupby('mode').agg({'profit': 'sum', 'product_id': 'count'})
mode_stats.columns = ['Total_Profit', 'Count']
print(mode_stats)

# Test 10: Date Functions
print("\n[TEST 10] DATE Functions (YEAR-MONTH)")
print("-" * 70)
df_with_profit['sale_date'] = pd.to_datetime(df_with_profit['sale_date'], errors='coerce')
df_with_profit['year_month'] = df_with_profit['sale_date'].dt.to_period('M')
print("Monthly Profit:")
monthly_profit = df_with_profit.groupby('year_month')['profit'].sum()
print(monthly_profit)

# Test 11: Export to CSV
print("\n[TEST 11] IMPORT/EXPORT - Save to CSV")
print("-" * 70)
data_processing.export_to_csv(df_with_profit, 'test_export.csv')
print("✓ Data exported to test_export.csv")
