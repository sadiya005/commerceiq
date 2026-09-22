from src.data_loader import load_all_data
from src.dataset_manager import dataset_manager


# ============================================================
# DEFAULT DATASET
# ============================================================

customer_data, product_data, order_data = load_all_data()

dataset_manager.customers = customer_data
dataset_manager.products = product_data
dataset_manager.orders = order_data


# ============================================================
# MERCHANDISE FILTER
# ============================================================

EXCLUDED_PRODUCT_KEYWORDS = [
    "POSTAGE",
    "DOTCOM POSTAGE",
    "BANK CHARGES",
    "SAMPLES",
    "BAD DEBT",
    "ADJUSTMENT",
    "MANUAL",
]


def is_merchandise_product(product_name):

    if pd_is_missing(product_name):
        return False

    name = str(product_name).upper()

    return not any(
        keyword in name
        for keyword in EXCLUDED_PRODUCT_KEYWORDS
    )


def pd_is_missing(value):
    return value is None or (
        isinstance(value, float)
        and value != value
    )


# ============================================================
# CUSTOMER
# ============================================================

def lookup_customer(customer_id):

    df = dataset_manager.customers

    matches = df[
        df["Customer ID"] == customer_id
    ]

    if matches.empty:
        return {
            "status": "not_found",
            "message": (
                f"Customer {customer_id} "
                "was not found."
            ),
        }

    row = matches.iloc[0]

    return {
        "status": "success",
        "customer_id": int(
            row["Customer ID"]
        ),
        "total_orders": int(
            row["Total_Orders"]
        ),
        "total_revenue": float(
            row["Total_Revenue"]
        ),
        "total_units": int(
            row["Total_Units"]
        ),
        "unique_products": int(
            row["Unique_Products"]
        ),
        "recency_days": int(
            row["Recency_Days"]
        ),
        "average_order_value": float(
            row["Average_Order_Value"]
        ),
        "revenue_segment": str(
            row["Revenue_Segment"]
        ),
        "activity_segment": str(
            row["Activity_Segment"]
        ),
    }


# ============================================================
# PRODUCT
# ============================================================

def lookup_product(stock_code):

    df = dataset_manager.products

    matches = df[
        df["StockCode"].astype(str)
        == str(stock_code)
    ]

    if matches.empty:
        return {
            "status": "not_found",
            "message": (
                f"Product {stock_code} "
                "was not found."
            ),
        }

    row = matches.iloc[0]

    return {
        "status": "success",
        "stock_code": str(
            row["StockCode"]
        ),
        "product_name": str(
            row["Product_Name"]
        ),
        "total_units_sold": int(
            row["Total_Units_Sold"]
        ),
        "total_revenue": float(
            row["Total_Revenue"]
        ),
        "orders": int(
            row["Orders"]
        ),
        "customers": int(
            row["Customers"]
        ),
        "average_price": float(
            row["Average_Price"]
        ),
        "customer_penetration": float(
            row["Customer_Penetration"]
        ),
        "revenue_segment": str(
            row["Revenue_Segment"]
        ),
    }


# ============================================================
# REVENUE
# ============================================================

def revenue_summary():

    customers = dataset_manager.customers
    products = dataset_manager.products
    orders = dataset_manager.orders

    return {
        "status": "success",
        "total_revenue": float(
            orders["Order_Revenue"].sum()
        ),
        "total_products": int(
            len(products)
        ),
        "total_customers": int(
            len(customers)
        ),
        "total_orders": int(
            len(orders)
        ),
    }


# ============================================================
# TOP PRODUCTS
# ============================================================

def top_revenue_products(top_k=5):

    products = dataset_manager.products.copy()

    products = products[
        products["Product_Name"].apply(
            is_merchandise_product
        )
    ]

    products = products.sort_values(
        "Total_Revenue",
        ascending=False,
    ).head(top_k)

    result = []

    for _, row in products.iterrows():

        result.append(
            {
                "stock_code": str(
                    row["StockCode"]
                ),
                "product_name": str(
                    row["Product_Name"]
                ),
                "total_revenue": float(
                    row["Total_Revenue"]
                ),
                "total_units_sold": int(
                    row["Total_Units_Sold"]
                ),
                "orders": int(
                    row["Orders"]
                ),
                "customers": int(
                    row["Customers"]
                ),
            }
        )

    return {
        "status": "success",
        "products": result,
    }