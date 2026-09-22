import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from src.analytics import (
    lookup_customer,
    lookup_product,
    revenue_summary,
    top_revenue_products
)


# Customer test
customer = lookup_customer(12346)

print("Customer 12346:")
print(customer)

assert customer["status"] == "success"
assert customer["customer_id"] == 12346
assert customer["total_revenue"] == 77183.60


# Product test
product = lookup_product("10002")

print("\nProduct 10002:")
print(product)

assert product["status"] == "success"
assert product["stock_code"] == "10002"
assert product["total_revenue"] == 759.89


# Revenue test
revenue = revenue_summary()

print("\nRevenue summary:")
print(revenue)

assert revenue["status"] == "success"
assert round(
    revenue["total_revenue"], 2
) == 10539552.83

assert revenue["total_customers"] == 4335
assert revenue["total_orders"] == 19865


# Top products test
top_products = top_revenue_products(5)

print("\nTop 5 merchandise products:")

for product in top_products["products"]:
    print(product)


expected_codes = [
    "22423",
    "23843",
    "85123A",
    "47566",
    "85099B"
]

actual_codes = [
    product["stock_code"]
    for product in top_products["products"]
]

assert actual_codes == expected_codes

print("\nAnalytics validation: PASS")