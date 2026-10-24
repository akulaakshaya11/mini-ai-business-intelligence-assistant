
from app.analytics import (
    total_revenue,
    top_product,
    monthly_revenue_trend,
    top_region,
    compare_months,
)

print("Total revenue:", total_revenue())
print("Top product:", top_product())
print("Monthly revenue trend:", monthly_revenue_trend())
print("Top region:", top_region())
print(
    "Month comparison:",
    compare_months("2026-04", "2026-05"),
)
