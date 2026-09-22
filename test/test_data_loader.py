import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from src.data_loader import load_all_data


customer_data, product_data, order_data = (
    load_all_data()
)


print("Customer data shape:", customer_data.shape)
print("Product data shape:", product_data.shape)
print("Order data shape:", order_data.shape)

print(
    "\nCustomer columns:",
    list(customer_data.columns)
)

print(
    "\nProduct columns:",
    list(product_data.columns)
)

print(
    "\nOrder columns:",
    list(order_data.columns)
)


assert len(customer_data) == 4335
assert len(product_data) == 3918
assert len(order_data) == 19865

print("\nData loader validation: PASS")
