
import sqlite3
import pandas as pd

from app.database import DB_PATH

# Check the source CSV
csv_df = pd.read_csv("data/sales_data.csv")

print("CSV rows:", len(csv_df))
print("CSV transaction IDs:", csv_df["Transaction_Id"].nunique())

# Check the database
with sqlite3.connect(DB_PATH) as conn:
    db_df = pd.read_sql_query(
        "SELECT * FROM sales", conn
    )

print("Database rows:", len(db_df))
print("Database transaction IDs:",
      db_df["Transaction_Id"].nunique())

print("\nTransactions in CSV but not in database:")
missing_ids = set(csv_df["Transaction_Id"]) - set(
    db_df["Transaction_Id"]
)
print(missing_ids)

print("\nMissing-price transactions in database:")
print(
    db_df[db_df["Unit_price"].isna()][
        ["Transaction_Id", "Unit_price", "Status"]
    ].to_string(index=False)
)

print("\nDatabase status counts:")
print(db_df["Status"].value_counts(dropna=False))
