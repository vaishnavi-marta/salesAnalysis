"""CustomTkinter dashboard for the Class 12 sales analysis project."""

from contextlib import redirect_stdout
import io
from pathlib import Path
import sys
import tkinter as tk
from tkinter import messagebox, ttk

import customtkinter as ctk
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import analysis
import data_processing
import visualization

COLORS = {
    "app": "#F4F7FB",
    "surface": "#FFFFFF",
    "sidebar": "#111827",
    "sidebar_hover": "#202B3D",
    "sidebar_active": "#334155",
    "ink": "#172033",
    "muted": "#697586",
    "line": "#E4E9F0",
    "accent": "#4F46E5",
    "accent_hover": "#4338CA",
    "teal": "#0F766E",
    "green": "#15803D",
    "red": "#B91C1C",
    "orange": "#C2410C",
    "soft_blue": "#EEF2FF",
}


class SalesAnalysisDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales & Profit Analysis | Class 12 IP")
        self.root.geometry("1360x880")
        self.root.minsize(1024, 700)
        self.root.configure(fg_color=COLORS["app"])
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.df_products = None
        self.df_sales = None
        self.df_merged = None
        self.current_plot = None
        self.active_visualization = None
        self.menu_buttons = {}
        self.active_menu_key = "home"
        self.menu_visible = True
        self.page_transition_id = None

        self.load_data()
        self._configure_table_style()
        self._create_layout()
        self.show_welcome()

    def load_data(self):
        try:
            self.df_products = data_processing.load_products()
            self.df_sales = data_processing.load_sales()
            self.df_merged = data_processing.add_profit_column()
        except Exception as error:
            messagebox.showerror("Data Loading Error", f"Failed to load data: {error}")
            self.root.after(0, self.root.destroy)
            raise

    def _configure_table_style(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure(
            "Dashboard.Treeview",
            background=COLORS["surface"],
            foreground=COLORS["ink"],
            fieldbackground=COLORS["surface"],
            rowheight=31,
            borderwidth=0,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Dashboard.Treeview.Heading",
            background="#F0F3F8",
            foreground=COLORS["ink"],
            relief="flat",
            anchor="center",
            font=("Segoe UI Semibold", 10),
        )
        style.map(
            "Dashboard.Treeview",
            background=[("selected", "#DCE5FF")],
            foreground=[("selected", COLORS["ink"])],
        )

    def _create_layout(self):
        self.header = ctk.CTkFrame(
            self.root, fg_color=COLORS["surface"], corner_radius=0, height=54
        )
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_propagate(False)
        self.header.grid_columnconfigure(1, weight=1)

        self.menu_toggle_btn = ctk.CTkButton(
            self.header,
            text="☰",
            width=38,
            height=34,
            corner_radius=10,
            fg_color=COLORS["soft_blue"],
            hover_color="#E0E7FF",
            text_color=COLORS["accent"],
            font=("Segoe UI", 17, "bold"),
            command=self.toggle_menu,
        )
        self.menu_toggle_btn.grid(row=0, column=0, padx=(16, 12), pady=10)

        ctk.CTkLabel(
            self.header,
            text="SALES ANALYSIS",
            text_color=COLORS["ink"],
            font=("Segoe UI", 14, "bold"),
        ).grid(row=0, column=1, sticky="w")

        self.header_status = ctk.CTkLabel(
            self.header,
            text=f"{len(self.df_sales):,} transactions  ·  {len(self.df_products):,} products",
            text_color=COLORS["muted"],
            font=("Segoe UI", 10),
        )
        self.header_status.grid(row=0, column=2, padx=20, sticky="e")

        ctk.CTkLabel(
            self.header,
            text="Vaishnavi Sai Marta",
            text_color=COLORS["ink"],
            font=("Segoe UI", 11, "bold"),
        ).grid(row=0, column=3, padx=(0, 20), sticky="e")

        self.workspace = ctk.CTkFrame(self.root, fg_color=COLORS["app"], corner_radius=0)
        self.workspace.grid(row=1, column=0, sticky="nsew")
        self.workspace.grid_rowconfigure(0, weight=1)
        self.workspace.grid_columnconfigure(1, weight=1)

        self.menu_frame = ctk.CTkFrame(
            self.workspace,
            width=220,
            fg_color=COLORS["sidebar"],
            corner_radius=0,
        )
        self.menu_frame.grid(row=0, column=0, sticky="ns")
        self.menu_frame.grid_propagate(False)
        self.menu_frame.grid_rowconfigure(7, weight=1)
        self.menu_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.menu_frame,
            text="WORKSPACE",
            text_color="#94A3B8",
            font=("Segoe UI", 10, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=18, pady=(20, 10))

        navigation = [
            ("⌂", "Home", self.show_welcome, "home"),
            ("▤", "Data Management", self.show_data_management, "data"),
            ("⌕", "Characteristic Analysis", self.show_analysis, "analysis"),
            ("◫", "Data Visualization", self.show_visualization, "visualization"),
            ("⇩", "Export Data", self.show_export, "export"),
        ]
        for row, (icon, label, command, key) in enumerate(navigation, start=1):
            button = ctk.CTkButton(
                self.menu_frame,
                text=f"{icon}    {label}",
                anchor="w",
                height=42,
                corner_radius=11,
                fg_color="transparent",
                hover_color=COLORS["sidebar_hover"],
                text_color="#E5E7EB",
                font=("Segoe UI", 12),
                command=lambda menu_key=key, callback=command: self._navigate(
                    menu_key, callback
                ),
            )
            button.grid(row=row, column=0, padx=12, pady=4, sticky="ew")
            self.menu_buttons[key] = button

        exit_button = ctk.CTkButton(
            self.menu_frame,
            text="×    Exit",
            anchor="w",
            height=42,
            corner_radius=11,
            fg_color="transparent",
            hover_color="#7F1D1D",
            text_color="#FCA5A5",
            font=("Segoe UI", 12),
            command=self.exit_app,
        )
        exit_button.grid(row=6, column=0, padx=12, pady=4, sticky="ew")

        ctk.CTkLabel(
            self.menu_frame,
            text="CLASS XII  ·  IP 065",
            text_color="#718096",
            font=("Segoe UI", 7, "bold"),
        ).grid(row=8, column=0, sticky="sw", padx=19, pady=18)

        self.content_frame = ctk.CTkFrame(
            self.workspace, fg_color=COLORS["app"], corner_radius=0
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

    def _navigate(self, key, callback):
        if self.page_transition_id is not None:
            self.root.after_cancel(self.page_transition_id)
            self.page_transition_id = None
        self.set_active_menu(key)
        self._fade_out(callback)

    def _fade_out(self, callback):
        try:
            alpha = float(self.root.attributes("-alpha"))
            if alpha > 0.82:
                self.root.attributes("-alpha", max(0.82, alpha - 0.09))
                self.page_transition_id = self.root.after(12, lambda: self._fade_out(callback))
                return
        except tk.TclError:
            callback()
            return
        callback()
        self._fade_in()

    def _fade_in(self):
        try:
            alpha = float(self.root.attributes("-alpha"))
            if alpha < 1.0:
                self.root.attributes("-alpha", min(1.0, alpha + 0.09))
                self.page_transition_id = self.root.after(12, self._fade_in)
            else:
                self.page_transition_id = None
        except tk.TclError:
            self.page_transition_id = None

    def set_active_menu(self, key):
        self.active_menu_key = key
        for current_key, button in self.menu_buttons.items():
            button.configure(
                fg_color=(
                    COLORS["sidebar_active"] if current_key == key else "transparent"
                ),
                text_color="#FFFFFF" if current_key == key else "#E5E7EB",
            )

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_frame.grid_remove()
        else:
            self.menu_frame.grid()
        self.menu_visible = not self.menu_visible
        self.menu_toggle_btn.configure(
            text="☰" if not self.menu_visible else "✕"
        )

    def _clear_content(self):
        if self.current_plot is not None:
            plt.close(self.current_plot.figure)
            self.current_plot = None
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _create_page(self, title, subtitle):
        self._clear_content()
        page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        page.grid(row=0, column=0, sticky="nsew", padx=18, pady=(8, 14))
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            page,
            text=title,
            text_color=COLORS["ink"],
            font=("Segoe UI", 24, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", pady=(0, 2))
        ctk.CTkLabel(
            page,
            text=subtitle,
            text_color=COLORS["muted"],
            font=("Segoe UI", 11),
            anchor="w",
        ).grid(row=1, column=0, sticky="ew", pady=(0, 13))
        return page

    def _card(self, parent, **grid_options):
        card = ctk.CTkFrame(
            parent,
            fg_color=COLORS["surface"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["line"],
        )
        card.grid(**grid_options)
        return card

    def _create_action_button(
        self, parent, text, command, color=COLORS["accent"], **grid_options
    ):
        button = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=39,
            corner_radius=11,
            fg_color=color,
            hover_color=COLORS["accent_hover"],
            text_color="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
        )
        button.grid(**grid_options)
        return button

    def show_welcome(self):
        self.set_active_menu("home")
        page = self._create_page(
            "Sales & Profit Overview",
            "A clear snapshot of product performance and sales channels.",
        )
        page.grid_rowconfigure(2, weight=0)
        page.grid_rowconfigure(3, weight=1)

        summary = self.df_merged
        total_profit = float(summary["profit"].sum())
        profit_by_mode = summary.groupby("mode")["profit"].sum()
        online_profit = float(profit_by_mode.get("Online", 0))
        offline_profit = float(profit_by_mode.get("Offline", 0))
        online_products = summary.loc[summary["mode"] == "Online"].groupby(
            "product_name"
        )["profit"].sum()
        offline_products = summary.loc[summary["mode"] == "Offline"].groupby(
            "product_name"
        )["profit"].sum()
        online_best = (
            f"Top: {online_products.idxmax()}"
            if not online_products.empty
            else "No online sales"
        )
        offline_best = (
            f"Top: {offline_products.idxmax()}"
            if not offline_products.empty
            else "No offline sales"
        )

        cards = ctk.CTkFrame(page, fg_color="transparent")
        cards.grid(row=2, column=0, sticky="new")
        for column in range(3):
            cards.grid_columnconfigure(column, weight=1, uniform="stats")

        stats = (
            ("TRANSACTIONS", f"{len(self.df_sales):,}", COLORS["accent"]),
            ("PRODUCTS", f"{len(self.df_products):,}", COLORS["teal"]),
            ("RECORDED PROFIT", f"₹{total_profit:,.2f}", COLORS["green"]),
        )
        for column, (label, value, accent) in enumerate(stats):
            card = self._card(
                cards,
                row=0,
                column=column,
                sticky="ew",
                padx=(0 if column == 0 else 7, 0 if column == 2 else 7),
                pady=(0, 12),
            )
            ctk.CTkLabel(
                card,
                text=label,
                text_color=COLORS["muted"],
                font=("Segoe UI", 10, "bold"),
            ).pack(anchor="w", padx=17, pady=(14, 3))
            ctk.CTkLabel(
                card,
                text=value,
                text_color=accent,
                font=("Segoe UI", 22, "bold"),
            ).pack(anchor="w", padx=17, pady=(0, 14))

        mode_card = self._card(cards, row=1, column=0, columnspan=3, sticky="ew")
        ctk.CTkLabel(
            mode_card,
            text="Profit by sales channel",
            text_color=COLORS["ink"],
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", padx=17, pady=(13, 8))
        channel_row = ctk.CTkFrame(mode_card, fg_color="transparent")
        channel_row.pack(fill="x", padx=17, pady=(0, 13))
        channel_row.grid_columnconfigure(0, weight=1)
        channel_row.grid_columnconfigure(1, weight=1)
        self._stat_line(channel_row, "Online profit", online_profit, 0, online_best)
        self._stat_line(channel_row, "Offline profit", offline_profit, 1, offline_best)

        best_products = (
            summary.groupby("product_name")["profit"].sum().sort_values(ascending=False)
        )
        best = best_products.head(5).rename_axis("Product").reset_index(name="Profit")
        best["Profit"] = best["Profit"].map(lambda value: f"₹{value:,.2f}")
        table_card = self._card(
            page,
            row=3,
            column=0,
            sticky="nsew",
            pady=(12, 0),
        )
        table_card.grid_rowconfigure(1, weight=1)
        table_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            table_card,
            text="Top five products by recorded profit",
            text_color=COLORS["ink"],
            font=("Segoe UI", 14, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=15, pady=(12, 6))
        self._fill_table(table_card, best, row=1, padx=12, pady=(0, 12))

    def _stat_line(self, parent, title, value, column, subtitle):
        frame = ctk.CTkFrame(
            parent, fg_color=COLORS["app"], corner_radius=11
        )
        frame.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 7, 7 if column == 0 else 0))
        ctk.CTkLabel(
            frame, text=title, text_color=COLORS["muted"], font=("Segoe UI", 10)
        ).pack(anchor="w", padx=12, pady=(9, 1))
        ctk.CTkLabel(
            frame,
            text=f"₹{value:,.2f}",
            text_color=COLORS["ink"],
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w", padx=12, pady=(0, 9))
        ctk.CTkLabel(
            frame,
            text=subtitle,
            text_color=COLORS["muted"],
            font=("Segoe UI", 9),
            wraplength=300,
            anchor="w",
        ).pack(anchor="w", padx=12, pady=(0, 9))

    def _create_data_page(self, key, title, buttons):
        self.set_active_menu(key)
        page = self._create_page(title, "Choose an action to explore the project data.")
        card = self._card(page, row=2, column=0, sticky="nsew")
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(1, weight=1)
        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.grid(row=0, column=0, sticky="ew", padx=13, pady=13)
        for column in range(3):
            actions.grid_columnconfigure(column, weight=1, uniform="actions")
        for index, (text, command) in enumerate(buttons):
            self._create_action_button(
                actions,
                text,
                command,
                row=index // 3,
                column=index % 3,
                sticky="ew",
                padx=5,
                pady=5,
            )
        self.create_results_area(card, row=1, column=0, padx=13, pady=(0, 13))

    def show_data_management(self):
        self._create_data_page(
            "data",
            "Data Management",
            [
                ("Show Products Data", self.show_products_data),
                ("Show Sales Data", self.show_sales_data),
                ("Show Profit Calculations", self.show_profit_data),
            ],
        )

    def show_analysis(self):
        functions = [
            ("Profit by Mode", analysis.profit_by_mode),
            ("Monthly Profit Trend", analysis.profit_by_month),
            ("Highest Profit Product", analysis.highest_profit_product),
            ("Lowest Profit Product", analysis.lowest_profit_product),
            ("Average Profit", analysis.average_profit),
            ("Total Profit", analysis.total_profit),
            ("Profit by Product & Mode", analysis.profit_by_product_and_mode),
            ("Profit by Product", analysis.profit_by_product),
            ("Smart Business Insights", analysis.smart_insights),
        ]
        self._create_data_page(
            "analysis",
            "Characteristic Analysis",
            [
                (label, lambda function=function: self.run_analysis(function))
                for label, function in functions
            ],
        )

    def show_visualization(self):
        self.set_active_menu("visualization")
        page = self._create_page(
            "Data Visualization",
            "Choose a chart. Axes are arranged horizontally for easier comparison and reading.",
        )
        page.grid_rowconfigure(2, weight=0)
        page.grid_rowconfigure(3, weight=1)

        chart_functions = [
            ("Profit by Product", visualization.bar_graph_profit_by_product),
            ("Online vs Offline Profit", visualization.bar_graph_profit_by_mode),
            ("Monthly Profit Trend", visualization.line_plot_monthly_trend),
            ("Quantity Distribution", visualization.histogram_quantity_distribution),
            ("Profit Distribution", visualization.histogram_profit_distribution),
            ("Quantity by Product", visualization.bar_graph_quantity_by_product),
        ]
        action_card = self._card(page, row=2, column=0, sticky="ew")
        for column in range(3):
            action_card.grid_columnconfigure(column, weight=1, uniform="chart-actions")
        for index, (label, function) in enumerate(chart_functions):
            self._create_action_button(
                action_card,
                label,
                lambda selected=function: self.run_visualization(selected),
                color=COLORS["accent"] if index < 3 else COLORS["teal"],
                row=index // 3,
                column=index % 3,
                sticky="ew",
                padx=7,
                pady=7,
            )
        self.chart_frame = ctk.CTkFrame(
            page,
            fg_color=COLORS["surface"],
            corner_radius=16,
            border_width=1,
            border_color=COLORS["line"],
        )
        self.chart_frame.grid(row=3, column=0, sticky="nsew", pady=(15, 0))
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.bind("<Configure>", self._position_chart_canvas)
        self._chart_placeholder()

    def _chart_placeholder(self):
        placeholder = ctk.CTkLabel(
            self.chart_frame,
            text="Select a chart above to view it here",
            text_color=COLORS["muted"],
            font=("Segoe UI", 13),
        )
        placeholder.place(relx=0.5, rely=0.5, anchor="center")

    def show_export(self):
        self.set_active_menu("export")
        page = self._create_page(
            "Export Data",
            "Save the processed sales data, including the recorded profit column, to CSV.",
        )
        card = self._card(page, row=2, column=0, sticky="new")
        ctk.CTkLabel(
            card,
            text="Export filename",
            text_color=COLORS["ink"],
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=18, pady=(18, 5))
        self.filename_entry = ctk.CTkEntry(
            card,
            width=360,
            height=40,
            corner_radius=10,
            border_color=COLORS["line"],
            placeholder_text="sales_with_profit.csv",
        )
        self.filename_entry.insert(0, "sales.csv")
        self.filename_entry.pack(anchor="w", padx=18, pady=5)
        export_button = ctk.CTkButton(
            card,
            text="Export to CSV",
            command=self.export_data,
            height=40,
            corner_radius=11,
            fg_color=COLORS["orange"],
            hover_color="#9A3412",
            font=("Segoe UI", 11, "bold"),
        )
        export_button.pack(anchor="w", padx=18, pady=(9, 18))

    def create_results_area(self, parent, row=0, column=0, padx=14, pady=14):
        results = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=12)
        results.grid(row=row, column=column, sticky="nsew", padx=padx, pady=pady)
        results.grid_rowconfigure(1, weight=1)
        results.grid_columnconfigure(0, weight=1)
        self.results_frame = results
        self.display_text_output(
            "Choose an action above to show the results here.", "RESULTS"
        )

    def _clear_results(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def _fill_table(self, parent, frame, row=0, padx=10, pady=10):
        table_frame = ctk.CTkFrame(parent, fg_color=COLORS["surface"], corner_radius=10)
        table_frame.grid(row=row, column=0, sticky="nsew", padx=padx, pady=pady)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        tree = ttk.Treeview(
            table_frame,
            columns=list(frame.columns),
            show="headings",
            style="Dashboard.Treeview",
        )
        for column in frame.columns:
            tree.heading(column, text=str(column), anchor="center")
            tree.column(column, anchor="center", width=145, minwidth=95, stretch=True)
        for values in frame.itertuples(index=False, name=None):
            tree.insert("", "end", values=tuple(self._format_value(value) for value in values))
        vertical = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        horizontal = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        return tree

    @staticmethod
    def _format_value(value):
        if pd.isna(value):
            return "—"
        if isinstance(value, float):
            return f"{value:,.2f}"
        return str(value)

    def display_dataframe(self, frame, title="DATA"):
        self._clear_results()
        self.results_frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(
            self.results_frame,
            text=f"{title}  ·  {len(frame):,} rows",
            text_color=COLORS["ink"],
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        self._fill_table(self.results_frame, frame, row=1, padx=8, pady=(0, 8))

    def display_text_output(self, text, title="RESULTS"):
        self._clear_results()
        ctk.CTkLabel(
            self.results_frame,
            text=title,
            text_color=COLORS["ink"],
            font=("Segoe UI", 13, "bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=12, pady=(10, 4))
        text_box = ctk.CTkTextbox(
            self.results_frame,
            corner_radius=10,
            fg_color="#F8FAFC",
            text_color=COLORS["ink"],
            font=("Consolas", 11),
            wrap="word",
        )
        text_box.grid(row=1, column=0, sticky="nsew", padx=8, pady=(0, 8))
        text_box.insert("1.0", text)
        text_box.configure(state="disabled")

    def show_products_data(self):
        self.display_dataframe(self.df_products.head(20), "PRODUCTS DATA (Top 20)")

    def show_sales_data(self):
        frame = self.df_sales
        if "mode" in frame.columns:
            online = frame[frame["mode"] == "Online"].head(10)
            offline = frame[frame["mode"] == "Offline"].head(10)
            frame = pd.concat([online, offline]).reset_index(drop=True)
        else:
            frame = frame.head(20)
        self.display_dataframe(frame, "SALES DATA (Sample 20)")

    def show_profit_data(self):
        if "product_id" in self.df_merged.columns:
            frame = self.df_merged.groupby(
                ["product_id", "product_name"], as_index=False
            )["profit"].sum()
        else:
            frame = self.df_merged.groupby(
                ["product_name"], as_index=False
            )["profit"].sum()
            frame.insert(0, "product_id", ["N/A"] * len(frame))
        frame = frame.sort_values("profit", ascending=False).head(20)
        self.display_dataframe(
            frame[["product_id", "product_name", "profit"]],
            "PRODUCT PROFIT SUMMARY (Top 20)",
        )

    def run_analysis(self, analysis_function):
        buffer = io.StringIO()
        result = None
        try:
            with redirect_stdout(buffer):
                result = analysis_function()
        except Exception as error:
            buffer.write(f"Error: {error}")

        output = buffer.getvalue().strip()
        title = analysis_function.__name__.upper().replace("_", " ")
        if isinstance(result, pd.DataFrame):
            self.display_dataframe(result, title)
        elif isinstance(result, pd.Series):
            frame = result.reset_index()
            if len(frame.columns) == 2:
                frame.columns = ["Category", "Value"]
            self.display_dataframe(frame, title)
        elif isinstance(result, dict):
            frame = pd.DataFrame(list(result.items()), columns=["Category", "Value"])
            self.display_dataframe(frame, title)
        else:
            self.display_text_output(output or str(result), title)

    def run_visualization(self, visualization_function):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        if self.current_plot is not None:
            plt.close(self.current_plot.figure)
            self.current_plot = None
        self.active_visualization = visualization_function

        figure_sizes = {
            visualization.bar_graph_profit_by_product: (12, 8),
            visualization.bar_graph_quantity_by_product: (12, 8),
            visualization.bar_graph_profit_by_mode: (8, 5),
            visualization.line_plot_monthly_trend: (8, 7),
            visualization.histogram_quantity_distribution: (8, 5.5),
            visualization.histogram_profit_distribution: (8, 5.5),
            visualization.pie_chart_profit_by_mode: (6, 6),
        }
        figure, axis = plt.subplots(
            figsize=figure_sizes.get(visualization_function, (8, 5.5)),
            dpi=100,
        )
        figure.patch.set_facecolor(COLORS["surface"])
        try:
            visualization_function(ax=axis)
            figure.tight_layout(pad=1.25)
        except Exception as error:
            plt.close(figure)
            messagebox.showerror(
                "Visualization Error", f"Failed to create chart: {error}"
            )
            self._chart_placeholder()
            return

        canvas = FigureCanvasTkAgg(figure, master=self.chart_frame)
        self.current_plot = canvas
        self._position_chart_canvas()

    def _position_chart_canvas(self, _event=None):
        if (
            self.current_plot is None
            or not self.current_plot.get_tk_widget().winfo_exists()
        ):
            return

        chart_widget = self.current_plot.get_tk_widget()
        available_width = self.chart_frame.winfo_width() - 12
        available_height = self.chart_frame.winfo_height() - 12
        if available_width < 100 or available_height < 100:
            return

        figure = self.current_plot.figure
        aspect_ratio = figure.get_figwidth() / figure.get_figheight()
        fill_canvas = self.active_visualization in (
            visualization.bar_graph_profit_by_product,
            visualization.bar_graph_quantity_by_product,
        )

        if fill_canvas:
            chart_width = available_width
            chart_height = available_height
        else:
            if available_width / available_height > aspect_ratio:
                chart_height = available_height
                chart_width = int(chart_height * aspect_ratio)
            else:
                chart_width = available_width
                chart_height = int(chart_width / aspect_ratio)

        chart_width = max(1, chart_width)
        chart_height = max(1, chart_height)
        dpi = figure.get_dpi()
        figure.set_size_inches(chart_width / dpi, chart_height / dpi, forward=False)
        if fill_canvas:
            figure.subplots_adjust(left=0.31, right=0.97, top=0.93, bottom=0.12)
        else:
            figure.tight_layout(pad=1.6)

        chart_widget.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=chart_width,
            height=chart_height,
        )
        self.current_plot.draw_idle()

    def export_data(self):
        filename = self.filename_entry.get().strip() or "sales_with_profit.csv"
        output_path = Path(filename).expanduser()
        if not output_path.is_absolute():
            output_path = Path.cwd() / output_path
        try:
            data_processing.export_to_csv(self.df_merged, str(output_path))
            messagebox.showinfo(
                "Export Success", f"Data exported successfully to {output_path}"
            )
        except Exception as error:
            messagebox.showerror("Export Error", f"Failed to export data: {error}")

    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


def main():
    root = ctk.CTk()
    SalesAnalysisDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()
