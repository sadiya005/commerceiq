import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from src.config import (
    PROJECT_ROOT,
    DATA_DIR,
    TEXT_MODEL,
    VISION_MODEL,
    CUSTOMER_DATA_PATH,
    PRODUCT_DATA_PATH,
    ORDER_DATA_PATH,
    validate_config
)


print("Project root:", PROJECT_ROOT)
print("Data directory:", DATA_DIR)

print("Text model:", TEXT_MODEL)
print("Vision model:", VISION_MODEL)

print(
    "Customer data exists:",
    CUSTOMER_DATA_PATH.exists()
)

print(
    "Product data exists:",
    PRODUCT_DATA_PATH.exists()
)

print(
    "Order data exists:",
    ORDER_DATA_PATH.exists()
)

print(
    "Configuration validation:",
    validate_config()
)
