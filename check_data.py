
import pandas as pd
from pathlib import Path

csv_path = Path("data/sales_data.csv")

if not csv_path.exists():
    raise FileNotFoundError(
        f"CSV not found at {csv_path.resolve()}"
    )

df = pd.read_csv(csv_path)

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst five records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nTransaction status counts:")
print(df["Status"].value_counts(dropna=False))
