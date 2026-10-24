
import pandas as pd

df = pd.read_csv("data/sales_data.csv")

required_columns = [
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

print("Original CSV rows:", len(df))

print("\nRows with missing required fields:")

invalid_rows = df[df[required_columns].isna().any(axis=1)]
print(invalid_rows.to_string(index=False))

print("\nDuplicate transaction IDs:")
print(
    df[df["Transaction_Id"].duplicated(keep=False)]
    .to_string(index=False)
)

print("\nRows with missing unit price:")
print(df[df["Unit_price"].isna()].to_string(index=False))

print("\nTransaction TXN0034:")
print(
    df[df["Transaction_Id"] == "TXN0034"].to_string(index=False)
)
