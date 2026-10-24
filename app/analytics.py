
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "sales.db"

# Common revenue definition:
# Completed transactions with a known price only.
REVENUE_FILTER = """
    Status = 'Completed'
    AND Unit_price IS NOT NULL
"""

REVENUE_EXPRESSION = """
    (Quantity * Unit_price) - Discount_amount
"""


def run_query(query, parameters=()):
    """Execute a read-only analytics query and return its rows."""
    connection = sqlite3.connect(
        f"file:{DB_PATH.as_posix()}?mode=ro",
        uri=True,
    )

    try:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(query, parameters)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        connection.close()


def total_revenue():
    """Calculate total revenue from eligible transactions."""
    query = f"""
        SELECT
            ROUND(COALESCE(SUM({REVENUE_EXPRESSION}), 0), 2)
            AS total_revenue
        FROM sales
        WHERE {REVENUE_FILTER}
    """
    return run_query(query)[0]["total_revenue"]


def top_product():
    """Find the product generating the highest revenue."""
    query = f"""
        SELECT
            Product AS product,
            ROUND(SUM({REVENUE_EXPRESSION}), 2) AS revenue
        FROM sales
        WHERE {REVENUE_FILTER}
        GROUP BY Product
        ORDER BY revenue DESC, Product ASC
        LIMIT 1
    """
    rows = run_query(query)
    return rows[0] if rows else None


def monthly_revenue_trend():
    """Calculate revenue grouped by calendar month."""
    query = f"""
        SELECT
            strftime('%Y-%m', Order_date) AS month,
            ROUND(SUM({REVENUE_EXPRESSION}), 2) AS revenue
        FROM sales
        WHERE {REVENUE_FILTER}
        GROUP BY strftime('%Y-%m', Order_date)
        ORDER BY month
    """
    return run_query(query)


def top_region():
    """Find the region generating the highest revenue."""
    query = f"""
        SELECT
            Region AS region,
            ROUND(SUM({REVENUE_EXPRESSION}), 2) AS revenue
        FROM sales
        WHERE {REVENUE_FILTER}
        GROUP BY Region
        ORDER BY revenue DESC, Region ASC
        LIMIT 1
    """
    rows = run_query(query)
    return rows[0] if rows else None


def compare_months(month_a, month_b):
    """Compare revenue between two months formatted as YYYY-MM."""
    query = f"""
        SELECT
            strftime('%Y-%m', Order_date) AS month,
            ROUND(SUM({REVENUE_EXPRESSION}), 2) AS revenue
        FROM sales
        WHERE {REVENUE_FILTER}
          AND strftime('%Y-%m', Order_date) IN (?, ?)
        GROUP BY strftime('%Y-%m', Order_date)
    """

    rows = run_query(query, (month_a, month_b))
    revenue_by_month = {
        row["month"]: row["revenue"] for row in rows
    }

    # Treat a month with no eligible transactions as zero revenue.
    revenue_a = revenue_by_month.get(month_a, 0)
    revenue_b = revenue_by_month.get(month_b, 0)

    difference = round(revenue_b - revenue_a, 2)

    if revenue_a != 0:
        percentage_change = round(
            (difference / revenue_a) * 100, 2
        )
    else:
        percentage_change = None

    return {
        "month_a": month_a,
        "revenue_a": revenue_a,
        "month_b": month_b,
        "revenue_b": revenue_b,
        "difference": difference,
        "percentage_change": percentage_change,
    }
