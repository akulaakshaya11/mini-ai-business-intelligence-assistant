
import sqlite3
from pathlib import Path

import pandas as pd


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "sales_data.csv"
DB_PATH = BASE_DIR / "sales.db"

REQUIRED_COLUMNS = [
    "Transaction_Id",
    "Order_date",
    "Product",
    "Category",
    "Region",
    "Sales_channel",
    "Quantity",
    "Unit_price",
    "Discount_amount",
    "Status",
]


def get_connection():
    """Create a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Validate the CSV, report data quality, and load valid records."""

    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Sales CSV not found: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    # Validate the CSV structure.
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    df = df[REQUIRED_COLUMNS].copy()

    original_rows = len(df)

    # Normalize text fields.
    text_columns = [
        "Transaction_Id",
        "Product",
        "Category",
        "Region",
        "Sales_channel",
        "Status",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()
        df[column] = df[column].replace("", pd.NA)

    # Parse dates and numeric fields.
    df["Order_date"] = pd.to_datetime(
        df["Order_date"],
        format="%d-%m-%Y",
        errors="coerce",
    )

    for column in ["Quantity", "Unit_price", "Discount_amount"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Remove records missing essential fields.
    # Unit_price is intentionally optional so missing-price records
    # can remain in the database for data-quality reporting.
    required_fields = [
        "Transaction_Id",
        "Order_date",
        "Product",
        "Category",
        "Region",
        "Sales_channel",
        "Quantity",
        "Discount_amount",
        "Status",
    ]

    missing_required = df[required_fields].isna().any(axis=1)
    missing_required_count = int(missing_required.sum())
    df = df.loc[~missing_required].copy()

    # Report invalid numeric values before filtering.
    invalid_quantity = df["Quantity"] <= 0
    invalid_discount = df["Discount_amount"] < 0
    invalid_price = (
        df["Unit_price"].notna() & (df["Unit_price"] < 0)
    )

    invalid_quantity_count = int(invalid_quantity.sum())
    invalid_discount_count = int(invalid_discount.sum())
    invalid_price_count = int(invalid_price.sum())

    print("\n--- Data Quality Report ---")
    print(f"Original CSV rows: {original_rows}")
    print(f"Rows missing required fields: {missing_required_count}")
    print(f"Rows with quantity <= 0: {invalid_quantity_count}")
    print(f"Rows with negative discount: {invalid_discount_count}")
    print(f"Rows with negative unit price: {invalid_price_count}")

    # Exclude rows that violate numeric rules.
    valid_price = df["Unit_price"].isna() | (df["Unit_price"] >= 0)

    df = df[
        (df["Quantity"] > 0)
        & (df["Discount_amount"] >= 0)
        & valid_price
    ].copy()

    # Transaction IDs must be unique.
    duplicate_count = int(df.duplicated(
        subset=["Transaction_Id"], keep="first"
    ).sum())

    df = df.drop_duplicates(
        subset=["Transaction_Id"],
        keep="first",
    )

    print(f"Duplicate transaction rows removed: {duplicate_count}")

    # Store dates consistently as YYYY-MM-DD.
    df["Order_date"] = df["Order_date"].dt.strftime("%Y-%m-%d")

    # Retain missing prices as SQL NULL.
    df["Unit_price"] = df["Unit_price"].astype(object)
    df["Unit_price"] = df["Unit_price"].where(
        pd.notna(df["Unit_price"]), None
    )

    # Load validated records into SQLite.
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                Transaction_Id TEXT PRIMARY KEY,
                Order_date TEXT NOT NULL,
                Product TEXT NOT NULL,
                Category TEXT NOT NULL,
                Region TEXT NOT NULL,
                Sales_channel TEXT NOT NULL,
                Quantity INTEGER NOT NULL CHECK (Quantity > 0),
                Unit_price REAL CHECK (
                    Unit_price IS NULL OR Unit_price >= 0
                ),
                Discount_amount REAL NOT NULL CHECK (
                    Discount_amount >= 0
                ),
                Status TEXT NOT NULL
            )
        """)

        # Reload the table so repeated initialization is reproducible.
        connection.execute("DELETE FROM sales")

        df.to_sql(
            "sales",
            connection,
            if_exists="append",
            index=False,
        )

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_date
            ON sales(Order_date)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_sales_product
            ON sales(Product)
        """)

        connection.commit()

        total_rows = connection.execute(
            "SELECT COUNT(*) FROM sales"
        ).fetchone()[0]

        eligible_rows = connection.execute("""
            SELECT COUNT(*)
            FROM sales
            WHERE Status = 'Completed'
              AND Unit_price IS NOT NULL
        """).fetchone()[0]

        missing_price_rows = connection.execute("""
            SELECT COUNT(*)
            FROM sales
            WHERE Unit_price IS NULL
        """).fetchone()[0]

        non_completed_rows = connection.execute("""
            SELECT COUNT(*)
            FROM sales
            WHERE Status != 'Completed'
        """).fetchone()[0]

    print("\n--- Database Summary ---")
    print("Database initialized successfully!")
    print(f"Original CSV rows: {original_rows}")
    print(f"Rows stored: {total_rows}")
    print(f"Rows eligible for revenue: {eligible_rows}")
    print(f"Rows with missing price: {missing_price_rows}")
    print(f"Non-completed rows: {non_completed_rows}")
    print(f"Rows excluded overall: {original_rows - total_rows}")
    print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    initialize_database()
