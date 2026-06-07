"""
GUI Dashboard using Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkfont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import io
from contextlib import redirect_stdout
import sys
import os
import pandas as pd

# Adding the scripts directory to the path 
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import data_processing
import analysis
import visualization

class SalesAnalysisDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Hybrid Sales & Profit Analysis System - Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#eef2ff')

        # Initializing data
        self.df_products = None
        self.df_sales = None
        self.df_merged = None
        self.load_data()

        # Initializing UI state
        self.current_plot = None
        self.menu_buttons = {}
        self.active_menu_key = None
        self.menu_visible = True
        self.font_family = self.get_font_family()

        # Creating main frames
        self.create_menu_toggle_button()
        self.create_menu_frame()
        self.create_content_frame()

    def load_data(self):
        #Loading data from CSV files
        try:
            self.df_products = data_processing.load_products()
            self.df_sales = data_processing.load_sales()
            self.df_merged = data_processing.add_profit_column()
        except Exception as e:
            messagebox.showerror("Data Loading Error", f"Failed to load data: {e}")
            sys.exit(1)

    def get_font_family(self):
        try:
            available = tkfont.families()
            return 'Satoshi' if 'Satoshi' in available else 'Arial'
        except Exception:
            return 'Arial'

    def create_menu_frame(self):
        # Creating the left menu panel and applying theme
        self.menu_frame = tk.Frame(self.root, width=250, bg='#E3E7ED')
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.menu_frame.pack_propagate(False)

        try:
            style = ttk.Style(self.root)
            style.theme_use('clam')
            style.configure('TButton', background='#ffffff', foreground='#1f2937', relief='flat')
            self.root.option_add('*Font', f'{self.font_family} 10')
        except Exception:
            pass

        title_label = tk.Label(self.menu_frame, text="MENU",
                      font=(self.font_family, 14, 'bold'), fg='#1f2937', bg='#E3E7ED')
        title_label.pack(pady=24)

        buttons = [
            ("🏠 Home", self.show_welcome, 'home'),
            ("📊 Data Management", self.show_data_management, 'data'),
            ("🔍 Characteristic Analysis", self.show_analysis, 'analysis'),
            ("📈 Data Visualization", self.show_visualization, 'visualization'),
            ("💾 Export Data", self.show_export, 'export'),
            ("❌ Exit", self.exit_app, 'exit')
        ]

        for text, command, key in buttons:
            btn = self.create_menu_button(self.menu_frame, text, command, key)
            btn.pack(pady=8, padx=16, fill=tk.X)

# Main Menu button creation
    def create_menu_button(self, parent, text, command, key):
        default_bg = '#E3E7ED'
        hover_bg = '#d1d5db'
        active_bg = '#ffffff'
        btn = tk.Button(parent, text=text, command=lambda: [self.set_active_menu(key), command()],
                       font=('Satoshi', 12, 'bold'), bg=default_bg, fg='#1f2937',
                       activebackground=active_bg, activeforeground='#1f2937',
                       relief=tk.FLAT, bd=0, padx=18, pady=14, anchor='w')
        btn.bind('<Enter>', lambda e: btn.configure(bg=hover_bg))
        btn.bind('<Leave>', lambda e: btn.configure(bg=active_bg if self.active_menu_key == key else default_bg))
        btn.bind('<ButtonPress>', lambda e: btn.configure(relief=tk.SUNKEN))
        btn.bind('<ButtonRelease>', lambda e: btn.configure(relief=tk.FLAT))
        self.menu_buttons[key] = btn
        return btn

    def set_active_menu(self, key):
        self.active_menu_key = key
        for current_key, btn in self.menu_buttons.items():
            if current_key == key:
                btn.configure(bg='#ffffff')
            else:
                btn.configure(bg='#E3E7ED')

    def create_menu_toggle_button(self):
        self.menu_toggle_btn = tk.Button(
            self.root,
            text='☰ Menu',
            command=self.toggle_menu,
            font=(self.font_family, 11, 'bold'),
            bg='#0f172a',
            fg='#ffffff',
            relief=tk.FLAT,
            bd=0,
            padx=16,
            pady=10,
            cursor='hand2'
        )
        self.menu_toggle_btn.pack(side=tk.TOP, anchor='nw', padx=10, pady=10)

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_frame.pack_forget()
            self.menu_visible = False
            self.menu_toggle_btn.config(text='☰ Menu')
        else:
            self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)
            self.menu_visible = True
            self.menu_toggle_btn.config(text='✕ Close')

    def create_action_button(self, parent, text, command, bg_color, active_color, width=22):
        btn = tk.Button(parent, text=text, command=command,
                       font=(self.font_family, 11, 'bold'), bg=bg_color, fg='#ffffff',
                       activebackground=active_color, activeforeground='#ffffff',
                       relief=tk.FLAT, bd=0, padx=18, pady=14, width=width)
        btn.configure(cursor='hand2')
        hover_bg = active_color
        normal_bg = bg_color
        btn.bind('<Enter>', lambda e: btn.configure(bg=hover_bg))
        btn.bind('<Leave>', lambda e: btn.configure(bg=normal_bg))
        btn.bind('<ButtonPress>', lambda e: btn.configure(relief=tk.SUNKEN))
        btn.bind('<ButtonRelease>', lambda e: btn.configure(relief=tk.FLAT))
        return btn

    def create_content_frame(self):
        """Create the main content area"""
        self.content_frame = tk.Frame(self.root, bg='#eef2ff')
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Welcome message
        self.show_welcome()

    def show_welcome(self):
        """Show welcome screen"""
        self.set_active_menu('home')
        self.clear_content()

        page_container = tk.Frame(self.content_frame, bg='#eef2ff')
        page_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        page_card = tk.Frame(page_container, bg='#ffffff', bd=0, highlightbackground='#dbe5f1', highlightthickness=1)
        page_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title = tk.Label(page_card, text="Welcome to Hybrid Sales and Profit Analysis System",
                        font=('Satoshi', 25, 'bold'), bg='#ffffff', fg='#0f172a')
        title.pack(pady=24)

        subtitle = tk.Label(page_card,
                           text="Analyze your hybrid sales with powerful insights and visualizations",
                           font=('Satoshi', 14), bg='#ffffff', fg='#475569')
        subtitle.pack(pady=(0, 24))

        # Quick stats
        stats_frame = tk.Frame(page_card, bg='#ffffff')
        stats_frame.pack(pady=10)

        try:
            total_sales = len(self.df_sales)
            total_products = len(self.df_products)
            total_profit = self.df_merged['profit'].sum()

            profit_by_mode = self.df_merged.groupby('mode')['profit'].sum()
            online_profit = profit_by_mode.get('Online', 0)
            offline_profit = profit_by_mode.get('Offline', 0)

            stats = [
                ("Total Sales", f"{total_sales:,}"),
                ("Total Products", f"{total_products:,}"),
                ("Total Profit", f"₹{total_profit:,.2f}")
            ]

            first_row = tk.Frame(stats_frame, bg='#ffffff')
            first_row.pack(pady=(0, 24), fill=tk.X)

            for label, value in stats:
                stat_card = tk.Frame(first_row, bg='#ffffff', bd=1, relief=tk.FLAT,
                                     highlightbackground='#dbe5f1', highlightthickness=1)
                stat_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10, ipadx=18, ipady=18)

                stat_label = tk.Label(stat_card, text=label, font=('Satoshi', 11, 'bold'),
                                      bg='#ffffff', fg='#475569')
                stat_label.pack()

                stat_value = tk.Label(stat_card, text=value, font=('Satoshi', 24, 'bold'),
                                      bg='#ffffff', fg='#0f766e')
                stat_value.pack(pady=(10, 0))

            second_row = tk.Frame(stats_frame, bg='#ffffff')
            second_row.pack(fill=tk.X)

            profit_stats = [
                ("Online Profit", f"₹{online_profit:,.2f}"),
                ("Offline Profit", f"₹{offline_profit:,.2f}")
            ]

            stat_frames = []
            for label, value in profit_stats:
                stat_card = tk.Frame(second_row, bg='#ffffff', bd=1, relief=tk.FLAT,
                                     highlightbackground='#dbe5f1', highlightthickness=1)
                stat_card.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10, ipadx=16, ipady=16)
                stat_frames.append(stat_card)

                stat_label = tk.Label(stat_card, text=label, font=('Satoshi', 11, 'bold'),
                                      bg='#ffffff', fg='#475569')
                stat_label.pack()

                stat_value = tk.Label(stat_card, text=value, font=('Satoshi', 22, 'bold'),
                                      bg='#ffffff', fg='#16a34a')
                stat_value.pack(pady=(8, 0))

            try:
                online_top = self.df_merged[self.df_merged['mode'] == 'Online'].groupby('product_name')['profit'].sum()
                if not online_top.empty:
                    online_best = online_top.idxmax()
                    online_best_val = online_top.max()
                else:
                    online_best = 'N/A'
                    online_best_val = 0

                offline_top = self.df_merged[self.df_merged['mode'] == 'Offline'].groupby('product_name')['profit'].sum()
                if not offline_top.empty:
                    offline_best = offline_top.idxmax()
                    offline_best_val = offline_top.max()
                else:
                    offline_best = 'N/A'
                    offline_best_val = 0

                best_labels = [
                    f"Top Online: {online_best} (₹{online_best_val:,.2f})",
                    f"Top Offline: {offline_best} (₹{offline_best_val:,.2f})"
                ]

                for sf, text in zip(stat_frames, best_labels):
                    sub = tk.Label(sf, text=text, font=('Satoshi', 10), bg='#ffffff', fg='#475569')
                    sub.pack(pady=(10,0))
            except Exception:
                pass

        except Exception as e:
            error_label = tk.Label(page_card, text=f"Error loading stats: {e}",
                                 font=('Satoshi', 12), bg='#ffffff', fg='#dc2626')
            error_label.pack(pady=20)

    def show_data_management(self):
        # Show data management options
        self.set_active_menu('data')
        self.clear_content()

        page_container = tk.Frame(self.content_frame, bg='#eef2ff')
        page_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        page_card = tk.Frame(page_container, bg='#ffffff', bd=0, highlightbackground='#dbe5f1', highlightthickness=1)
        page_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title = tk.Label(page_card, text="📊 Data Management",
                        font=('Satoshi', 20, 'bold'), bg='#ffffff', fg='#0f172a')
        title.pack(pady=20)

        buttons_frame = tk.Frame(page_card, bg='#ffffff')
        buttons_frame.pack(pady=10)

        buttons = [
            ("Show Products Data", self.show_products_data),
            ("Show Sales Data", self.show_sales_data),
            ("Show Profit Calculations", self.show_profit_data)
        ]

        for i, (text, command) in enumerate(buttons):
            btn = self.create_action_button(buttons_frame, text, command, '#3A7DFF', '#2563EB', width=24)
            btn.grid(row=i//3, column=i%3, padx=12, pady=12)

        self.create_results_area(page_card)

    def show_analysis(self):
        # Show analysis query options
        self.set_active_menu('analysis')
        self.clear_content()

        page_container = tk.Frame(self.content_frame, bg='#eef2ff')
        page_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        page_card = tk.Frame(page_container, bg='#ffffff', bd=0, highlightbackground='#dbe5f1', highlightthickness=1)
        page_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title = tk.Label(page_card, text="🔍 Characteristic Analysis",
                        font=('Satoshi', 20, 'bold'), bg='#ffffff', fg='#0f172a')
        title.pack(pady=20)

        buttons_frame = tk.Frame(page_card, bg='#ffffff')
        buttons_frame.pack(pady=10)

        buttons = [
            ("Profit by Mode", lambda: self.run_analysis(analysis.profit_by_mode)),
            ("Monthly Profit Trend", lambda: self.run_analysis(analysis.profit_by_month)),
            ("Highest Profit Product", lambda: self.run_analysis(analysis.highest_profit_product)),
            ("Lowest Profit Product", lambda: self.run_analysis(analysis.lowest_profit_product)),
            ("Average Profit", lambda: self.run_analysis(analysis.average_profit)),
            ("Total Profit", lambda: self.run_analysis(analysis.total_profit)),
            ("Profit by Product & Mode", lambda: self.run_analysis(analysis.profit_by_product_and_mode)),
            ("Profit by Product", lambda: self.run_analysis(analysis.profit_by_product)),
            ("Smart Business Insights", lambda: self.run_analysis(analysis.smart_insights))
        ]

        for i, (text, command) in enumerate(buttons):
            btn = self.create_action_button(buttons_frame, text, command, '#FF5C5C', '#E63946', width=24)
            btn.grid(row=i//3, column=i%3, padx=12, pady=12)

        self.create_results_area(page_card)

    def show_visualization(self):
        # Show visualization options
        self.set_active_menu('visualization')
        self.clear_content()

        page_container = tk.Frame(self.content_frame, bg='#eef2ff')
        page_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        page_card = tk.Frame(page_container, bg='#ffffff', bd=0, highlightbackground='#dbe5f1', highlightthickness=1)
        page_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title = tk.Label(page_card, text="📈 Data Visualization",
                        font=('Satoshi', 20, 'bold'), bg='#ffffff', fg='#0f172a')
        title.pack(pady=20)

        buttons_frame = tk.Frame(page_card, bg='#ffffff')
        buttons_frame.pack(pady=10)

        buttons = [
            ("Profit by Product", lambda: self.run_visualization(visualization.bar_graph_profit_by_product)),
            ("Online vs Offline Profit", lambda: self.run_visualization(visualization.bar_graph_profit_by_mode)),
            ("Monthly Profit Trend", lambda: self.run_visualization(visualization.line_plot_monthly_trend)),
            ("Quantity Distribution", lambda: self.run_visualization(visualization.histogram_quantity_distribution)),
            ("Profit Distribution", lambda: self.run_visualization(visualization.histogram_profit_distribution)),
            ("Quantity by Product", lambda: self.run_visualization(visualization.bar_graph_quantity_by_product))
        ]

        for i, (text, command) in enumerate(buttons):
            btn = self.create_action_button(buttons_frame, text, command, '#2ECC71', '#16A34A', width=24)
            btn.grid(row=i//3, column=i%3, padx=16, pady=14)

        # Chart area
        self.chart_frame = tk.Frame(page_card, bg='#ffffff')
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def show_export(self):
        # Show export options
        self.set_active_menu('export')
        self.clear_content()

        page_container = tk.Frame(self.content_frame, bg='#eef2ff')
        page_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        page_card = tk.Frame(page_container, bg='#ffffff', bd=0, highlightbackground='#dbe5f1', highlightthickness=1)
        page_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        title = tk.Label(page_card, text="💾 Export Data to CSV",
                        font=('Satoshi', 20, 'bold'), bg='#ffffff', fg='#0f172a')
        title.pack(pady=24)

        export_frame = tk.Frame(page_card, bg='#ffffff')
        export_frame.pack(pady=40)

        filename_label = tk.Label(export_frame, text="Enter filename:",
                                font=('Satoshi', 13), bg='#ffffff', fg='#475569')
        filename_label.pack(pady=10)

        self.filename_entry = tk.Entry(export_frame, font=('Satoshi', 13), width=32, bd=1, relief=tk.SOLID)
        self.filename_entry.insert(0, "sales.csv")
        self.filename_entry.pack(pady=10, ipady=8)

        export_btn = self.create_action_button(export_frame, "Export to CSV", self.export_data, '#F39C12', '#EA7C12', width=28)
        export_btn.configure(font=('Satoshi', 14, 'bold'))
        export_btn.pack(pady=24)

    def create_results_area(self, parent):
        self.results_frame = tk.Frame(parent, bg='#ffffff')
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        results_label = tk.Label(self.results_frame, text="Results:",
                               font=('Satoshi', 13, 'bold'), bg='#ffffff', fg='#0f172a')
        results_label.pack(anchor=tk.W, pady=(0,12))

        self.results_text = scrolledtext.ScrolledText(self.results_frame,
                                                    font=('Satoshi', 12),
                                                    bg='#f8fafc', fg='#000000',
                                                    wrap=tk.WORD, bd=1, relief=tk.SOLID,
                                                    highlightthickness=1, highlightbackground='#dbe5f1', insertbackground='#000000')
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.results_text.config(height=24)

    def display_dataframe(self, df, title="DATA"):
        
        # Clear previous content
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Title
        label = tk.Label(self.results_frame, text=title,
                        font=('Satoshi', 14, 'bold'),
                        bg='#ffffff', fg='#0f172a')
        label.pack(anchor='w', pady=(0, 10))

        # Create Treeview
        tree = ttk.Treeview(self.results_frame, show='headings')

        # Define columns 
        tree['columns'] = list(df.columns)

        for col in df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor='center', width=130)

        # Insert data
        for _, row in df.iterrows():
            tree.insert('', 'end', values=list(row))

        # Scrollbars
        y_scroll = ttk.Scrollbar(self.results_frame, orient='vertical', command=tree.yview)
        x_scroll = ttk.Scrollbar(self.results_frame, orient='horizontal', command=tree.xview)

        tree.configure(yscroll=y_scroll.set, xscroll=x_scroll.set)

        tree.pack(fill='both', expand=True, side='left')
        y_scroll.pack(fill='y', side='right')
        x_scroll.pack(fill='x', side='bottom')

    def display_text_output(self, text, title="RESULTS"):
        # Clear previous content
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Title
        label = tk.Label(self.results_frame, text=title,
                        font=('Satoshi', 14, 'bold'),
                        bg='#ffffff', fg='#0f172a')
        label.pack(anchor='w', pady=(0, 10))

        # Text box
        text_box = scrolledtext.ScrolledText(
            self.results_frame,
            font=('Satoshi', 12),
            bg='#f8fafc', fg='#000000',
            wrap=tk.WORD, bd=1, relief=tk.SOLID
        )
        text_box.pack(fill=tk.BOTH, expand=True)

        text_box.insert(tk.END, text)
            
    def clear_content(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Clear any existing plot
        if self.current_plot:
            plt.close('all')
            self.current_plot = None

    def show_products_data(self):
        # Display at least 20 product records
        df = self.df_products.head(20)
        self.display_dataframe(df, "PRODUCTS DATA (Top 20)")

    def show_sales_data(self):
        # Display at least 20 sales records and include both modes when available
        df = self.df_sales.copy()
        if 'mode' in df.columns:
            online = df[df['mode'] == 'Online'].head(10)
            offline = df[df['mode'] == 'Offline'].head(10)
            df = pd.concat([online, offline]).reset_index(drop=True)
        else:
            df = df.head(20)
        self.display_dataframe(df, "SALES DATA (Sample 20)")

    def show_profit_data(self):
        # Simplified profit view: product_id, product_name, profit
        if 'product_id' in self.df_merged.columns:
            df = self.df_merged.groupby(['product_id', 'product_name'], as_index=False)['profit'].sum()
        else:
            df = self.df_merged.groupby(['product_name'], as_index=False)['profit'].sum()
            df.insert(0, 'product_id', ['N/A'] * len(df))
        df = df.sort_values('profit', ascending=False).head(20)
        self.display_dataframe(df[['product_id', 'product_name', 'profit']], "PRODUCT PROFIT SUMMARY (Top 20)")


    def run_analysis(self, analysis_function):
        f = io.StringIO()
        result = None
        with redirect_stdout(f):
            try:
                result = analysis_function()
            except Exception as e:
                print(f"Error: {e}")

        output = f.getvalue().strip()
        title = analysis_function.__name__.upper().replace('_', ' ')

        if isinstance(result, pd.DataFrame):
            self.display_dataframe(result, title)
        elif isinstance(result, pd.Series):
            df = result.reset_index()
            df.columns = ['Category', 'Value'] if len(df.columns) == 2 else list(df.columns)
            self.display_dataframe(df, title)
        elif isinstance(result, dict):
            df = pd.DataFrame(list(result.items()), columns=['Category', 'Value'])
            self.display_dataframe(df, title)
        elif output:
            self.display_text_output(output, title)
        else:
            self.display_text_output(str(result), title)

    def run_visualization(self, viz_function):
        # Run visualization function and display chart
        # Clear previous plot
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        # Close previous canvas-based plot if present
        if self.current_plot:
            try:
                self.current_plot.get_tk_widget().destroy()
            except Exception:
                pass
            plt.close('all')
            self.current_plot = None

        # Create a figure and axes sized for embedding (smaller square)
        fig, ax = plt.subplots(figsize=(4.5, 4.5))

        try:
            # Call visualization function that draws on the provided Axes
            result = viz_function(ax=ax)
        except TypeError:
            # Fallback: some older viz functions may not accept ax kwarg
            try:
                viz_function(ax)
            except Exception as e:
                messagebox.showerror("Visualization Error", f"Failed to create chart: {e}")
                plt.close(fig)
                return
        except Exception as e:
            messagebox.showerror("Visualization Error", f"Failed to create chart: {e}")
            plt.close(fig)
            return

        # Final layout adjustments
        try:
            fig.tight_layout(pad=1.0)
        except Exception:
            pass

        # Embed the plot in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        self.current_plot = canvas

    def export_data(self):
        # Export data to CSV
        filename = self.filename_entry.get().strip()
        if not filename:
            filename = "sales_with_profit.csv"

        try:
            data_processing.export_to_csv(self.df_merged, filename)
            messagebox.showinfo("Export Success", f"Data exported successfully to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data: {e}")

    def exit_app(self):
        #Exit the application
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = SalesAnalysisDashboard(root)
    root.mainloop()

if __name__ == '__main__':
    main()