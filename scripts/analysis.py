import pandas as pd
from data_processing import add_profit_column

def profit_by_product():
    """SQL equivalent: GROUP BY product, SUM profit"""
    df = add_profit_column()
    # GROUP BY product_name, SUM profit
    result = df.groupby('product_name')['profit'].sum().sort_values(ascending=False)
    print("\n=== PROFIT BY PRODUCT ===")
    for product, profit in result.items():
        print(f"{product}: ₹{profit:.2f}")
    return result

def profit_by_mode():
    """SQL equivalent: GROUP BY mode, SUM profit"""
    df = add_profit_column()
    # GROUP BY mode, SUM profit
    result = df.groupby('mode')['profit'].sum()
    print("\n=== PROFIT BY MODE (Online vs Offline) ===")
    for mode, profit in result.items():
        print(f"{mode}: ₹{profit:.2f}")
    
    # Calculate percentage
    total = result.sum()
    for mode, profit in result.items():
        pct = (profit / total) * 100
        print(f"{mode} Contribution: {pct:.1f}%")
    
    return result

def profit_by_month():
    """SQL equivalent: GROUP BY year and month, SUM profit"""
    df = add_profit_column()
    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    df = df.dropna(subset=['sale_date'])
    df['year_month'] = df['sale_date'].dt.to_period('M')
    result = df.groupby('year_month')['profit'].sum()
    print("\n=== MONTHLY PROFIT TREND ===")
    for year_month, profit in result.items():
        print(f"{year_month}: ₹{profit:.2f}")
    
    return result

def highest_profit_product():
    """SQL equivalent: SELECT MAX(profit) by product"""
    df = add_profit_column()
    result = df.groupby('product_name')['profit'].sum().idxmax()
    max_profit = df.groupby('product_name')['profit'].sum().max()
    print(f"\n=== HIGHEST PROFIT PRODUCT ===")
    print(f"{result}: ₹{max_profit:.2f}")
    return result, max_profit

def lowest_profit_product():
    """SQL equivalent: SELECT MIN(profit) by product"""
    df = add_profit_column()
    result = df.groupby('product_name')['profit'].sum().idxmin()
    min_profit = df.groupby('product_name')['profit'].sum().min()
    print(f"\n=== LOWEST PROFIT PRODUCT ===")
    print(f"{result}: ₹{min_profit:.2f}")
    return result, min_profit

def average_profit():
    """SQL equivalent: AVG(profit)"""
    df = add_profit_column()
    avg_profit = df['profit'].mean()
    print(f"\n=== AVERAGE PROFIT PER TRANSACTION ===")
    print(f"₹{avg_profit:.2f}")
    return avg_profit

def total_profit():
    """SQL equivalent: SUM(profit)"""
    df = add_profit_column()
    total = df['profit'].sum()
    print(f"\n=== TOTAL PROFIT ===")
    print(f"₹{total:.2f}")
    return total

def total_quantity_sold():
    """SQL equivalent: SUM(quantity), COUNT"""
    df = add_profit_column()
    total_qty = df['quantity'].sum()
    count = df.shape[0]  # COUNT(*)
    print(f"\n=== SALES STATISTICS ===")
    print(f"Total Quantity Sold: {total_qty}")
    print(f"Total Transactions: {count}")
    return total_qty, count

def profit_by_product_and_mode():
    """SQL equivalent: GROUP BY product, mode, SUM profit"""
    df = add_profit_column()
    # GROUP BY product_name and mode
    result = df.groupby(['product_name', 'mode'])['profit'].sum()
    print("\n=== PROFIT BY PRODUCT AND MODE ===")
    print(result)
    return result

def smart_insights():
    """Business insights from analysis"""
    df = add_profit_column()
    total = df['profit'].sum()
    
    print("\n=== SMART BUSINESS INSIGHTS ===")
    
    # Most profitable
    profit_by_prod = df.groupby('product_name')['profit'].sum()
    top_product = profit_by_prod.idxmax()
    top_profit = profit_by_prod.max()
    contribution = (top_profit / total) * 100
    print(f"► {top_product} contributes {contribution:.1f}% of total profit (₹{top_profit:.2f})")
    
    # Online vs Offline
    profit_by_mode_result = df.groupby('mode')['profit'].sum()
    if len(profit_by_mode_result) == 2:
        if profit_by_mode_result['Online'] > profit_by_mode_result['Offline']:
            print(f"► Online sales are more profitable (₹{profit_by_mode_result['Online']:.2f} vs ₹{profit_by_mode_result['Offline']:.2f})")
        else:
            print(f"► Offline sales are more profitable (₹{profit_by_mode_result['Offline']:.2f} vs ₹{profit_by_mode_result['Online']:.2f})")
    
    # Average profit
    avg_p = df['profit'].mean()
    print(f"► Average profit per transaction: ₹{avg_p:.2f}")
    
    # Products below average
    below_avg = profit_by_prod[profit_by_prod < avg_p * df.groupby('product_name').size().mean()]
    if len(below_avg) > 0:
        worst_product = below_avg.idxmin()
        print(f"► Consider reviewing strategy for {worst_product} (low profit)")
