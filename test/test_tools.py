import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from src.tools import (
    AVAILABLE_FUNCTIONS,
    TOOL_SCHEMAS,
    execute_tool
)


print("Available tools:")
print(list(AVAILABLE_FUNCTIONS.keys()))

print(
    "\nNumber of tool schemas:",
    len(TOOL_SCHEMAS)
)


# Customer tool
customer_result = execute_tool(
    "lookup_customer",
    {"customer_id": 12346}
)

print("\nCustomer tool result:")
print(customer_result)

assert customer_result["status"] == "success"
assert customer_result["customer_id"] == 12346


# Product tool
product_result = execute_tool(
    "lookup_product",
    {"stock_code": "10002"}
)

print("\nProduct tool result:")
print(product_result)

assert product_result["status"] == "success"
assert product_result["stock_code"] == "10002"


# Revenue tool
revenue_result = execute_tool(
    "revenue_summary"
)

print("\nRevenue tool result:")
print(revenue_result)

assert revenue_result["status"] == "success"
assert round(
    revenue_result["total_revenue"], 2
) == 10539552.83


# Top-product tool
top_result = execute_tool(
    "top_revenue_products",
    {"top_k": 3}
)

print("\nTop-product tool result:")
print(top_result)

assert top_result["status"] == "success"
assert len(top_result["products"]) == 3


print("\nTool execution validation: PASS")