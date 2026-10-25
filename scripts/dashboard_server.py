"""Create a self-contained HTML dashboard from the project CSV files."""

from html import escape
from io import StringIO
from pathlib import Path
import sys
import webbrowser

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent
DASHBOARD_PATH = SCRIPT_DIR / "dashboard.html"

sys.path.insert(0, str(SCRIPT_DIR))
import data_processing


def _format_money(value):
    return f"₹{value:,.2f}"


def _table(frame, columns, headings):
    display = frame.loc[:, columns].copy()
    display.columns = headings
    return display.to_html(
        index=False,
        border=0,
        classes="data-table",
        escape=True,
        na_rep="—",
    )


def _chart_svg(chart_type, transactions, product_profit, mode_profit, monthly_profit):
    figure, axis = plt.subplots(figsize=(8, 3.8))
    figure.patch.set_facecolor("#ffffff")
    axis.set_facecolor("#ffffff")
    axis.spines[["top", "right"]].set_visible(False)

    if chart_type == "products":
        top_products = product_profit.head(10).sort_values()
        axis.barh(top_products.index.astype(str), top_products.values, color="#4f46e5")
        axis.set_xlabel("Total profit (₹)")
        axis.set_title("Top 10 Products by Profit")
        axis.grid(axis="x", alpha=0.18)
    elif chart_type == "channels":
        axis.pie(
            mode_profit.values,
            labels=mode_profit.index.astype(str),
            autopct="%1.1f%%",
            startangle=90,
            colors=["#4f46e5", "#06b6d4"],
            wedgeprops={"width": 0.44, "edgecolor": "white"},
        )
        axis.set_title("Profit Share by Sales Mode")
        axis.axis("equal")
    elif chart_type == "monthly":
        positions = range(len(monthly_profit))
        axis.plot(positions, monthly_profit.values, color="#4f46e5", marker="o", markersize=3)
        spacing = max(1, (len(monthly_profit) + 9) // 10)
        ticks = list(range(0, len(monthly_profit), spacing))
        axis.set_xticks(ticks)
        axis.set_xticklabels(
            [str(monthly_profit.index[position]) for position in ticks],
            rotation=35,
            ha="right",
        )
        axis.set_ylabel("Total profit (₹)")
        axis.set_title("Monthly Profit Trend (Year-Month)")
        axis.grid(axis="y", alpha=0.18)
    else:
        axis.hist(
            transactions["profit"].dropna(),
            bins=30,
            color="#06b6d4",
            edgecolor="white",
        )
        axis.set_xlabel("Profit per transaction (₹)")
        axis.set_ylabel("Number of transactions")
        axis.set_title("Transaction Profit Distribution")
        axis.grid(axis="y", alpha=0.18)

    figure.tight_layout()
    buffer = StringIO()
    figure.savefig(buffer, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(figure)
    svg = buffer.getvalue()
    return svg[svg.find("<svg") : svg.rfind("</svg>") + len("</svg>")]


def build_dashboard_html():
    products = data_processing.load_products()
    sales = data_processing.load_sales()
    transactions = data_processing.add_profit_column()

    product_profit = (
        transactions.groupby("product_name")["profit"]
        .sum()
        .sort_values(ascending=False)
    )
    mode_profit = transactions.groupby("mode")["profit"].sum().sort_values(ascending=False)
    monthly = transactions.copy()
    monthly["sale_date"] = pd.to_datetime(monthly["sale_date"], errors="coerce")
    monthly = monthly.dropna(subset=["sale_date"])
    monthly["year_month"] = monthly["sale_date"].dt.to_period("M")
    monthly_profit = monthly.groupby("year_month")["profit"].sum()

    dates = pd.to_datetime(sales["sale_date"], errors="coerce").dropna()
    missing_source_price = int(pd.to_numeric(sales["price"], errors="coerce").isna().sum())
    missing_display_price = int(transactions["selling_price"].isna().sum())
    average_profit = float(transactions["profit"].mean()) if len(transactions) else 0.0

    product_rows = transactions.groupby("product_name", as_index=False)["profit"].sum()
    product_rows = product_rows.sort_values("profit", ascending=False).head(15)
    product_rows["profit"] = product_rows["profit"].map(_format_money)

    sales_sample = transactions[
        ["sale_id", "product_name", "quantity", "mode", "sale_date", "profit"]
    ].head(15).copy()
    sales_sample["sale_date"] = pd.to_datetime(
        sales_sample["sale_date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")
    sales_sample["profit"] = sales_sample["profit"].map(_format_money)

    mode_rows = pd.DataFrame(
        {
            "Sales mode": mode_profit.index,
            "Profit": mode_profit.map(_format_money).values,
        }
    )
    charts = {
        "products": _chart_svg(
            "products", transactions, product_profit, mode_profit, monthly_profit
        ),
        "channels": _chart_svg(
            "channels", transactions, product_profit, mode_profit, monthly_profit
        ),
        "monthly": _chart_svg(
            "monthly", transactions, product_profit, mode_profit, monthly_profit
        ),
        "distribution": _chart_svg(
            "distribution", transactions, product_profit, mode_profit, monthly_profit
        ),
    }
    date_label = (
        f"{dates.min():%d %b %Y} – {dates.max():%d %b %Y}" if not dates.empty else "No valid dates"
    )
    warning = (
        f"{missing_source_price:,} source rows have no sale price; product average "
        f"price fills most gaps. {missing_display_price:,} rows still have no "
        "selling price."
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sales &amp; Profit Analysis Dashboard</title>
  <style>
    :root {{ color-scheme: light; --ink:#172033; --muted:#68738a; --line:#e7eaf1; --accent:#4f46e5; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; background:#f5f7fb; color:var(--ink); font:15px/1.5 "Segoe UI",Arial,sans-serif; }}
    .layout {{ min-height:100vh; display:grid; grid-template-columns:235px minmax(0,1fr); }}
    aside {{ background:#111827; color:white; padding:28px 18px; }}
    .brand {{ font-size:17px; font-weight:700; margin:0 8px 7px; }}
    .brand-note {{ color:#aab4c5; font-size:12px; margin:0 8px 28px; }}
    nav {{ display:grid; gap:6px; }}
    nav a {{ color:#d7deea; text-decoration:none; padding:10px 11px; border-radius:8px; }}
    nav a:hover {{ background:#263247; color:white; }}
    main {{ max-width:1450px; width:100%; padding:32px clamp(18px,4vw,55px); margin:auto; }}
    .eyebrow {{ color:var(--accent); font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; }}
    h1 {{ font-size:30px; line-height:1.2; margin:5px 0 7px; }}
    h2 {{ font-size:20px; margin:0; }}
    .subtle {{ color:var(--muted); margin:0; }}
    .cards {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:15px; margin:24px 0; }}
    .card,.panel {{ background:white; border:1px solid var(--line); border-radius:13px; box-shadow:0 3px 12px #17203308; }}
    .card {{ padding:18px; }}
    .card-label {{ color:var(--muted); font-size:13px; }}
    .card-value {{ font-size:24px; font-weight:700; margin-top:6px; }}
    .panel {{ padding:21px; margin:18px 0; }}
    .panel-heading {{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:13px; }}
    .grid-2 {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; }}
    .chart {{ width:100%; overflow:hidden; }}
    .chart svg {{ width:100%; height:auto; display:block; }}
    .table-wrap {{ overflow:auto; max-height:570px; }}
    .data-table {{ border-collapse:collapse; width:100%; font-size:13px; }}
    .data-table th,.data-table td {{ padding:10px 12px; border-bottom:1px solid var(--line); text-align:left; }}
    .data-table th {{ background:#f7f8fc; position:sticky; top:0; z-index:1; }}
    .search {{ border:1px solid var(--line); border-radius:8px; padding:9px 11px; min-width:190px; font:inherit; }}
    .notice {{ border:1px solid #f2d38d; border-radius:10px; background:#fff9e9; color:#79540b; padding:12px 15px; margin:18px 0; }}
    section {{ scroll-margin-top:16px; }}
    footer {{ color:var(--muted); font-size:12px; text-align:center; padding:20px; }}
    @media(max-width:900px) {{ .cards {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
    @media(max-width:650px) {{
      .layout {{ grid-template-columns:1fr; }}
      aside {{ padding:15px; }}
      .brand-note {{ margin-bottom:12px; }}
      nav {{ display:flex; overflow:auto; }}
      nav a {{ white-space:nowrap; }}
      main {{ padding:22px 14px; }}
      .cards,.grid-2 {{ grid-template-columns:1fr; }}
      .card-value {{ font-size:21px; }}
      .panel-heading {{ align-items:flex-start; flex-direction:column; }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside>
      <div class="brand">Sales Analysis</div>
      <div class="brand-note">Class 12 Informatics Practices · CSV project</div>
      <nav aria-label="Dashboard sections">
        <a href="#overview">Overview</a>
        <a href="#products">Products</a>
        <a href="#channels">Sales modes</a>
        <a href="#monthly">Monthly trend</a>
        <a href="#transactions">Transactions</a>
      </nav>
    </aside>
    <main>
      <section id="overview">
        <div class="eyebrow">Business performance</div>
        <h1>Sales &amp; Profit Dashboard</h1>
        <p class="subtle">Summary generated from the project CSV files · Sale dates: {escape(date_label)}</p>
        <div class="cards">
          <div class="card"><div class="card-label">Transactions</div><div class="card-value">{len(sales):,}</div></div>
          <div class="card"><div class="card-label">Products</div><div class="card-value">{len(products):,}</div></div>
          <div class="card"><div class="card-label">Total recorded profit</div><div class="card-value">{_format_money(float(transactions["profit"].sum()))}</div></div>
          <div class="card"><div class="card-label">Average profit / transaction</div><div class="card-value">{_format_money(average_profit)}</div></div>
        </div>
        <div class="notice"><strong>Data note:</strong> {escape(warning)} Profit totals use the profit values in the sales CSV.</div>
      </section>
      <section id="products">
        <div class="grid-2">
          <div class="panel"><div class="panel-heading"><h2>Product profit</h2></div><div class="chart">{charts["products"]}</div></div>
          <div class="panel"><div class="panel-heading"><h2>Top products</h2></div><div class="table-wrap">{_table(product_rows, ["product_name", "profit"], ["Product", "Total profit"])}</div></div>
        </div>
      </section>
      <section id="channels">
        <div class="grid-2">
          <div class="panel"><div class="panel-heading"><h2>Sales channel contribution</h2></div><div class="chart">{charts["channels"]}</div></div>
          <div class="panel"><div class="panel-heading"><h2>Profit by sales mode</h2></div><div class="table-wrap">{_table(mode_rows, ["Sales mode", "Profit"], ["Sales mode", "Recorded profit"])}</div></div>
        </div>
      </section>
      <section id="monthly">
        <div class="grid-2">
          <div class="panel"><div class="panel-heading"><h2>Monthly profit trend</h2><span class="subtle">{len(monthly_profit)} year-month periods</span></div><div class="chart">{charts["monthly"]}</div></div>
          <div class="panel"><div class="panel-heading"><h2>Transaction profit distribution</h2></div><div class="chart">{charts["distribution"]}</div></div>
        </div>
      </section>
      <section id="transactions">
        <div class="panel">
          <div class="panel-heading"><h2>Sales transaction sample</h2><input class="search" type="search" placeholder="Filter these rows…" aria-label="Filter transaction sample"></div>
          <p class="subtle">Showing the first 15 transactions from the CSV file.</p>
          <div class="table-wrap">{_table(sales_sample, ["sale_id", "product_name", "quantity", "mode", "sale_date", "profit"], ["Sale ID", "Product", "Quantity", "Mode", "Date", "Profit"])}</div>
        </div>
      </section>
      <footer>Created locally from CSV data with Python, Pandas and Matplotlib. No web service or JSON API is used.</footer>
    </main>
  </div>
  <script>
    const filter = document.querySelector(".search");
    const rows = document.querySelectorAll("#transactions tbody tr");
    filter.addEventListener("input", function () {{
      const query = this.value.toLowerCase();
      rows.forEach(function (row) {{
        row.hidden = !row.textContent.toLowerCase().includes(query);
      }});
    }});
  </script>
</body>
</html>
"""
    return html


def main():
    dashboard_html = build_dashboard_html()
    DASHBOARD_PATH.write_text(dashboard_html, encoding="utf-8")
    print(f"Sales dashboard created: {DASHBOARD_PATH}")
    if not webbrowser.open(DASHBOARD_PATH.as_uri()):
        print(f"Open this file in your browser: {DASHBOARD_PATH}")


if __name__ == "__main__":
    main()
