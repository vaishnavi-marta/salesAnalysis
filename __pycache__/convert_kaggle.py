import pandas as pd

df = pd.read_csv('your_kaggle_file.csv')

# Normalize dates
df['sale_date'] = pd.to_datetime(df['Purchase_Date'], dayfirst=True, errors='coerce').dt.strftime('%Y-%m-%d')

# Map payment method to mode
def map_mode(pm):
    pm = str(pm).strip().lower()
    if 'cash' in pm or 'cod' in pm:
        return 'Offline'
    return 'Online'

df['mode'] = df['Payment_Method'].apply(map_mode)
df['quantity'] = 1

# Build product table
products = (
    df[['Product_ID', 'Category', 'Price (Rs.)', 'Final_Price(Rs.)']]
    .drop_duplicates('Product_ID')
    .reset_index(drop=True)
)
products['product_id'] = products.index + 1
products['product_name'] = products['Category'] + ' ' + (products.index + 1).astype(str)
products['cost_price'] = (products['Price (Rs.)'] * 0.60).round(2)
products['selling_price'] = products['Final_Price(Rs.)'].round(2)

products_csv = products[['product_id', 'product_name', 'cost_price', 'selling_price']]
products_csv.to_csv('products.csv', index=False)

# Build sales table
sales = df.merge(products[['Product_ID', 'product_id']], on='Product_ID', how='left')
sales['sale_id'] = range(1, len(sales) + 1)
sales_csv = sales[['sale_id', 'product_id', 'quantity', 'mode', 'sale_date']]
sales_csv.to_csv('sales.csv', index=False)

print('Created products.csv and sales.csv')