from scripts import data_processing

print('Loading products and sales...')
df_products = data_processing.load_products()
df_sales = data_processing.load_sales()
df_merged = data_processing.add_profit_column()
print('Products:', df_products.shape)
print('Sales:', df_sales.shape)
print('Merged:', df_merged.shape)
print(df_merged.columns.tolist())
print(df_merged[['product_name','selling_price','cost_price','profit']].head())
