import matplotlib.pyplot as plt
import pandas as pd
from textwrap import fill
from data_processing import add_profit_column


def _ensure_ax(ax, figsize=(6, 5)):
    """Helper: return (fig, ax, created_flag) where created_flag True when we created the figure."""
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
        return fig, ax, True
    else:
        return None, ax, False


def bar_graph_profit_by_product(ax=None):
    """BAR GRAPH: Product vs Profit. Shows top 10 and bottom 10 products."""
    df = add_profit_column()
    profit_by_product = df.groupby('product_name')['profit'].sum().sort_values(ascending=False)
    
    # Get top 10 and bottom 10
    top_10 = profit_by_product.head(10)
    bottom_10 = profit_by_product.tail(10)
    display_data = pd.concat([top_10, bottom_10])

    fig, ax, created = _ensure_ax(ax, figsize=(12, 8))
    
    # Color top 10 differently from bottom 10
    colors = ['#1f77b4' if prod in top_10.index else '#ff7f0e' for prod in display_data.index]

    ax.barh(range(len(display_data)), display_data.values, color=colors, edgecolor='black')
    ax.set_xlabel('Profit (₹)', fontsize=10, fontweight='bold')
    ax.set_ylabel('Product Name', fontsize=10, fontweight='bold')
    ax.set_title('Profit by Product (Top 10 & Bottom 10)', fontsize=13, fontweight='bold')
    ax.set_yticks(range(len(display_data)))
    ax.set_yticklabels([fill(str(name), width=34) for name in display_data.index], fontsize=8)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.25)

    if created:
        fig.tight_layout()
        return fig
    return None


def bar_graph_profit_by_mode(ax=None):
    """BAR GRAPH: Online vs Offline Profit. Colors use green palette for both modes."""
    df = add_profit_column()
    profit_by_mode = df.groupby('mode')['profit'].sum()

    fig, ax, created = _ensure_ax(ax, figsize=(8, 5))

    # Ensure Online and Offline are colored green shades (Online primary green)
    color_map = {'Online': '#27ae60', 'Offline': '#2ecc71'}
    colors = [color_map.get(m, '#27ae60') for m in profit_by_mode.index]

    ax.barh(profit_by_mode.index, profit_by_mode.values, color=colors, edgecolor='black')
    ax.set_xlabel('Profit (₹)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Sales Mode', fontsize=13, fontweight='bold')
    ax.set_title('Profit: Online vs Offline', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.25)

    if created:
        fig.tight_layout()
        return fig
    return None


def pie_chart_profit_by_mode(ax=None):
    """PIE CHART: Profit contribution from each sales mode."""
    df = add_profit_column()
    profit_by_mode = df.groupby('mode')['profit'].sum()
    if profit_by_mode.empty or (profit_by_mode < 0).any() or profit_by_mode.sum() <= 0:
        raise ValueError(
            "The profit-by-mode pie chart requires positive total profit "
            "and non-negative profit for every sales mode."
        )

    fig, ax, created = _ensure_ax(ax, figsize=(5, 5))
    ax.pie(
        profit_by_mode.values,
        labels=profit_by_mode.index,
        autopct='%1.1f%%',
        startangle=90,
    )
    ax.set_title('Profit Contribution by Sales Mode', fontsize=13, fontweight='bold')
    ax.axis('equal')

    if created:
        fig.tight_layout()
        return fig
    return None


def line_plot_monthly_trend(ax=None):
    """LINE PLOT: Monthly Profit Trend"""
    df = add_profit_column()
    if 'sale_date' not in df.columns:
        raise ValueError("Missing required column: sale_date")

    df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
    df = df.dropna(subset=['sale_date'])
    df['year_month'] = df['sale_date'].dt.to_period('M')
    monthly_profit = df.groupby('year_month')['profit'].sum()
    if monthly_profit.empty:
        raise ValueError("No monthly profit data available for plotting")

    fig, ax, created = _ensure_ax(ax, figsize=(5, 4))

    month_positions = range(len(monthly_profit))
    ax.plot(monthly_profit.values, month_positions, marker='o', linewidth=2, color='blue')
    ax.set_xlabel('Profit (₹)', fontsize=11, fontweight='bold')
    ax.set_ylabel('Year and month', fontsize=11, fontweight='bold')
    ax.set_title('Monthly Profit Trend', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.25)
    tick_spacing = max(1, (len(monthly_profit) + 9) // 10)
    tick_positions = list(range(0, len(monthly_profit), tick_spacing))
    ax.set_yticks(tick_positions)
    ax.set_yticklabels(
        [str(monthly_profit.index[position]) for position in tick_positions],
    )
    ax.invert_yaxis()

    if created:
        fig.tight_layout()
        return fig
    return None


def histogram_quantity_distribution(ax=None):
    """HISTOGRAM: Distribution of Quantity Sold"""
    df = add_profit_column()

    fig, ax, created = _ensure_ax(ax, figsize=(5, 4))

    ax.hist(df['quantity'], bins=5, color='coral', edgecolor='black', alpha=0.8, orientation='horizontal')
    ax.set_xlabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_ylabel('Quantity Sold', fontsize=11, fontweight='bold')
    ax.set_title('Distribution of Quantity Sold per Transaction', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.25)

    if created:
        fig.tight_layout()
        return fig
    return None


def histogram_profit_distribution(ax=None):
    """HISTOGRAM: Distribution of Profit per Transaction"""
    df = add_profit_column()

    fig, ax, created = _ensure_ax(ax, figsize=(5, 4))

    ax.hist(df['profit'], bins=8, color='lightgreen', edgecolor='black', alpha=0.8, orientation='horizontal')
    ax.set_xlabel('Frequency', fontsize=11, fontweight='bold')
    ax.set_ylabel('Profit (₹)', fontsize=11, fontweight='bold')
    ax.set_title('Distribution of Profit per Transaction', fontsize=13, fontweight='bold')
    ax.grid(axis='x', alpha=0.25)

    if created:
        fig.tight_layout()
        return fig
    return None


def bar_graph_quantity_by_product(ax=None):
    """BAR GRAPH: Quantity Sold per Product. Shows top 10 and bottom 10 products."""
    df = add_profit_column()
    qty_by_product = df.groupby('product_name')['quantity'].sum().sort_values(ascending=False)
    
    # Get top 10 and bottom 10
    top_10 = qty_by_product.head(10)
    bottom_10 = qty_by_product.tail(10)
    display_data = pd.concat([top_10, bottom_10])

    fig, ax, created = _ensure_ax(ax, figsize=(12, 8))
    
    # Color top 10 differently from bottom 10
    colors = ['#2ca02c' if prod in top_10.index else '#d62728' for prod in display_data.index]

    ax.barh(range(len(display_data)), display_data.values, color=colors, edgecolor='black')
    ax.set_xlabel('Total Quantity Sold', fontsize=10, fontweight='bold')
    ax.set_ylabel('Product Name', fontsize=10, fontweight='bold')
    ax.set_title('Quantity Sold by Product (Top 10 & Bottom 10)', fontsize=13, fontweight='bold')
    ax.set_yticks(range(len(display_data)))
    ax.set_yticklabels([fill(str(name), width=34) for name in display_data.index], fontsize=8)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.25)

    if created:
        fig.tight_layout()
        return fig
    return None
