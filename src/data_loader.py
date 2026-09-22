import pandas as pd

from src.config import (
    CUSTOMER_DATA_PATH,
    PRODUCT_DATA_PATH,
    ORDER_DATA_PATH
)


def load_customer_data():
    """Load customer-level CommerceIQ features."""
    
    return pd.read_csv(
        CUSTOMER_DATA_PATH
    )


def load_product_data():
    """Load product-level CommerceIQ features."""
    
    return pd.read_csv(
        PRODUCT_DATA_PATH
    )


def load_order_data():
    """Load order-level CommerceIQ analytics."""
    
    return pd.read_csv(
        ORDER_DATA_PATH
    )


def load_all_data():
    """Load all CommerceIQ datasets."""
    
    customer_data = load_customer_data()
    product_data = load_product_data()
    order_data = load_order_data()

    return (
        customer_data,
        product_data,
        order_data
    )