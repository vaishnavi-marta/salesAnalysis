#!/usr/bin/env python3
"""
Uses:
- Pandas: DataFrame creation from CSV, head(), tail(), selection, indexing, boolean indexing, groupby
- Matplotlib: Line plots, bar graphs, histograms with customization
- Python: Basic operations and menu-driven interface
"""

import matplotlib.pyplot as plt

import data_processing
import analysis
import visualization


def _show_chart(chart_function):
    chart_function()
    plt.show()


def main_menu():
    """Main menu for the application"""
    while True:
        print("\n" + "="*60)
        print("      HYBRID SALES AND PROFIT ANALYSIS SYSTEM")
        print("="*60)
        print("\n1. Data Management")
        print("2. Analysis Queries")
        print("3. Data Visualization")
        print("4. Export Data")
        print("5. Exit")
        print("\n" + "-"*60)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            data_management_menu()
        elif choice == '2':
            analysis_menu()
        elif choice == '3':
            visualization_menu()
        elif choice == '4':
            export_menu()
        elif choice == '5':
            print("\nThank you for using the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def data_management_menu():
    """Data Management Menu - Demonstrates Pandas operations"""
    while True:
        print("\n" + "-"*60)
        print("DATA MANAGEMENT (Pandas Operations)")
        print("-"*60)
        print("\n1. Display Products (head/tail)")
        print("2. Display Sales (head/tail)")
        print("3. Show Merged Data with Profit")
        print("4. Selection and Indexing Demo")
        print("5. Boolean Indexing (High Profit Filter)")
        print("6. Rename Columns Demo")
        print("7. Series Operations")
        print("8. Back to Main Menu")
        print("\n" + "-"*60)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            df_products = data_processing.load_products()
            print("\n--- PRODUCTS DATA (head and tail) ---")
            print("\nFIRST 3 PRODUCTS (head):")
            print(df_products.head(3))
            print("\nLAST 2 PRODUCTS (tail):")
            print(df_products.tail(2))
        
        elif choice == '2':
            df_sales = data_processing.load_sales()
            print("\n--- SALES DATA (head and tail) ---")
            print("\nFIRST 5 SALES (head):")
            print(df_sales.head(5))
            print("\nLAST 3 SALES (tail):")
            print(df_sales.tail(3))
        
        elif choice == '3':
            df_merged = data_processing.add_profit_column()
            print("\n--- MERGED DATA WITH PROFIT CALCULATION ---")
            display_columns = [
                column for column in
                ('product_name', 'quantity', 'selling_price', 'profit')
                if column in df_merged.columns
            ]
            print(df_merged[display_columns].head(7))
        
        elif choice == '4':
            df = data_processing.add_profit_column()
            data_processing.selection_and_indexing(df)
        
        elif choice == '5':
            df = data_processing.add_profit_column()
            data_processing.boolean_indexing(df)
        
        elif choice == '6':
            df = data_processing.add_profit_column()
            data_processing.rename_columns(df)
        
        elif choice == '7':
            data_processing.series_operations()
        
        elif choice == '8':
            break
        
        else:
            print("Invalid choice. Please try again.")

def analysis_menu():
    """Analysis Menu - SQL-like queries using Pandas"""
    while True:
        print("\n" + "-"*60)
        print("ANALYSIS QUERIES (SQL Functions using Pandas)")
        print("-"*60)
        print("\n1. Profit by Product (GROUP BY + SUM)")
        print("2. Profit by Mode (GROUP BY + SUM)")
        print("3. Monthly Profit Trend (GROUP BY MONTH)")
        print("4. Highest Profit Product (MAX)")
        print("5. Lowest Profit Product (MIN)")
        print("6. Average Profit (AVG)")
        print("7. Total Profit (SUM)")
        print("8. Sales Statistics (COUNT + SUM)")
        print("9. Profit by Product and Mode (Multiple GROUP BY)")
        print("10. Smart Business Insights")
        print("11. Back to Main Menu")
        print("\n" + "-"*60)
        
        choice = input("Enter your choice (1-11): ").strip()
        
        if choice == '1':
            analysis.profit_by_product()
        elif choice == '2':
            analysis.profit_by_mode()
        elif choice == '3':
            analysis.profit_by_month()
        elif choice == '4':
            analysis.highest_profit_product()
        elif choice == '5':
            analysis.lowest_profit_product()
        elif choice == '6':
            analysis.average_profit()
        elif choice == '7':
            analysis.total_profit()
        elif choice == '8':
            analysis.total_quantity_sold()
        elif choice == '9':
            analysis.profit_by_product_and_mode()
        elif choice == '10':
            analysis.smart_insights()
        elif choice == '11':
            break
        else:
            print("Invalid choice. Please try again.")

def visualization_menu():
    """Visualization Menu - Matplotlib plots"""
    while True:
        print("\n" + "-"*60)
        print("DATA VISUALIZATION (Matplotlib - Line, Bar, Histogram, Pie)")
        print("-"*60)
        print("\n1. Bar Graph - Profit by Product")
        print("2. Bar Graph - Online vs Offline Profit")
        print("3. Line Plot - Monthly Profit Trend")
        print("4. Histogram - Quantity Distribution")
        print("5. Histogram - Profit Distribution")
        print("6. Bar Graph - Quantity Sold by Product")
        print("7. Pie Chart - Profit by Sales Mode")
        print("8. Back to Main Menu")
        print("\n" + "-"*60)
        
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == '1':
            _show_chart(visualization.bar_graph_profit_by_product)
        elif choice == '2':
            _show_chart(visualization.bar_graph_profit_by_mode)
        elif choice == '3':
            _show_chart(visualization.line_plot_monthly_trend)
        elif choice == '4':
            _show_chart(visualization.histogram_quantity_distribution)
        elif choice == '5':
            _show_chart(visualization.histogram_profit_distribution)
        elif choice == '6':
            _show_chart(visualization.bar_graph_quantity_by_product)
        elif choice == '7':
            _show_chart(visualization.pie_chart_profit_by_mode)
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

def export_menu():
    """Export Menu - Export data to CSV"""
    print("\n" + "-"*60)
    print("EXPORT DATA TO CSV")
    print("-"*60)
    
    df_with_profit = data_processing.add_profit_column()
    filename = input("\nEnter filename to export (default: sales_with_profit.csv): ").strip()
    
    if not filename:
        filename = "sales_with_profit.csv"
    
    try:
        data_processing.export_to_csv(df_with_profit, filename)
        print(f"Successfully exported to {filename}")
    except Exception as e:
        print(f"Error exporting file: {e}")

if __name__ == '__main__':
    main_menu()