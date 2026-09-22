import pandas as pd


REQUIRED_COLUMNS = [
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country",
]


class DatasetManager:

    def __init__(self):
        self.transactions = None
        self.customers = None
        self.products = None
        self.orders = None
        self.dataset_name = "Default CommerceIQ Dataset"

    def validate_columns(self, df):
        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            return {
                "valid": False,
                "missing_columns": missing_columns,
            }

        return {
            "valid": True,
            "missing_columns": [],
        }

    def load_dataset(
        self,
        df,
        dataset_name="Uploaded Dataset",
    ):

        # ----------------------------------------------------
        # Validate required columns
        # ----------------------------------------------------

        validation = self.validate_columns(df)

        if not validation["valid"]:
            raise ValueError(
                "Missing required columns: "
                + ", ".join(
                    validation["missing_columns"]
                )
            )

        # Work on a copy so the original DataFrame
        # supplied by the caller is not modified.
        df = df.copy()

        # ----------------------------------------------------
        # Clean text columns
        # ----------------------------------------------------

        text_columns = [
            "Invoice",
            "StockCode",
            "Description",
            "Country",
        ]

        for column in text_columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

        # ----------------------------------------------------
        # Basic type conversion
        # ----------------------------------------------------

        df["InvoiceDate"] = pd.to_datetime(
            df["InvoiceDate"],
            errors="coerce",
        )

        df["Quantity"] = pd.to_numeric(
            df["Quantity"],
            errors="coerce",
        )

        df["Price"] = pd.to_numeric(
            df["Price"],
            errors="coerce",
        )

        df["Customer ID"] = pd.to_numeric(
            df["Customer ID"],
            errors="coerce",
        )

        # ----------------------------------------------------
        # Remove unusable transaction rows
        # ----------------------------------------------------

        df = df.dropna(
            subset=[
                "Invoice",
                "StockCode",
                "Quantity",
                "Price",
                "InvoiceDate",
            ]
        ).copy()

        # ----------------------------------------------------
        # Revenue
        # ----------------------------------------------------

        df["Revenue"] = (
            df["Quantity"] * df["Price"]
        )

        # ----------------------------------------------------
        # Customer analytics
        # ----------------------------------------------------

        customer_df = df.dropna(
            subset=["Customer ID"]
        ).copy()

        if len(customer_df) > 0:

            customer_features = (
                customer_df
                .groupby("Customer ID")
                .agg(
                    Total_Orders=(
                        "Invoice",
                        "nunique",
                    ),
                    Total_Revenue=(
                        "Revenue",
                        "sum",
                    ),
                    Total_Units=(
                        "Quantity",
                        "sum",
                    ),
                    Unique_Products=(
                        "StockCode",
                        "nunique",
                    ),
                    Last_Order_Date=(
                        "InvoiceDate",
                        "max",
                    ),
                    First_Order_Date=(
                        "InvoiceDate",
                        "min",
                    ),
                )
                .reset_index()
            )

            reference_date = (
                df["InvoiceDate"].max()
            )

            customer_features[
                "Recency_Days"
            ] = (
                reference_date
                - customer_features[
                    "Last_Order_Date"
                ]
            ).dt.days

            customer_features[
                "Customer_Lifetime_Days"
            ] = (
                customer_features[
                    "Last_Order_Date"
                ]
                - customer_features[
                    "First_Order_Date"
                ]
            ).dt.days

            customer_features[
                "Average_Order_Value"
            ] = (
                customer_features[
                    "Total_Revenue"
                ]
                / customer_features[
                    "Total_Orders"
                ]
            )

            customer_features[
                "Average_Units_Per_Order"
            ] = (
                customer_features[
                    "Total_Units"
                ]
                / customer_features[
                    "Total_Orders"
                ]
            )

            customer_features[
                "Average_Products_Per_Order"
            ] = (
                customer_features[
                    "Unique_Products"
                ]
                / customer_features[
                    "Total_Orders"
                ]
            )

            customer_features[
                "Orders_Per_Month"
            ] = (
                customer_features[
                    "Total_Orders"
                ]
                / (
                    customer_features[
                        "Customer_Lifetime_Days"
                    ].clip(lower=1)
                    / 30
                )
            )

            customer_features[
                "Revenue_Segment"
            ] = pd.qcut(
                customer_features[
                    "Total_Revenue"
                ].rank(method="first"),
                q=4,
                labels=[
                    "Low",
                    "Medium",
                    "High",
                    "Very High",
                ],
            )

            customer_features[
                "Activity_Segment"
            ] = pd.cut(
                customer_features[
                    "Recency_Days"
                ],
                bins=[
                    -1,
                    30,
                    90,
                    float("inf"),
                ],
                labels=[
                    "Active",
                    "Recently Inactive",
                    "Inactive",
                ],
            )

            self.customers = (
                customer_features
                .drop(
                    columns=[
                        "Last_Order_Date",
                        "First_Order_Date",
                    ]
                )
            )

        else:
            self.customers = pd.DataFrame()

        # ----------------------------------------------------
        # Product analytics
        # ----------------------------------------------------

        product_features = (
            df.groupby(
                [
                    "StockCode",
                    "Description",
                ]
            )
            .agg(
                Total_Units_Sold=(
                    "Quantity",
                    "sum",
                ),
                Total_Revenue=(
                    "Revenue",
                    "sum",
                ),
                Orders=(
                    "Invoice",
                    "nunique",
                ),
                Customers=(
                    "Customer ID",
                    "nunique",
                ),
                Average_Price=(
                    "Price",
                    "mean",
                ),
            )
            .reset_index()
        )

        product_features[
            "Revenue_Per_Order"
        ] = (
            product_features[
                "Total_Revenue"
            ]
            / product_features[
                "Orders"
            ]
        )

        product_features[
            "Units_Per_Order"
        ] = (
            product_features[
                "Total_Units_Sold"
            ]
            / product_features[
                "Orders"
            ]
        )

        customer_count = (
            customer_df[
                "Customer ID"
            ].nunique()
        )

        if customer_count > 0:

            product_features[
                "Customer_Penetration"
            ] = (
                product_features[
                    "Customers"
                ]
                / customer_count
            )

        else:

            product_features[
                "Customer_Penetration"
            ] = 0

        product_features[
            "Revenue_Segment"
        ] = pd.qcut(
            product_features[
                "Total_Revenue"
            ].rank(method="first"),
            q=4,
            labels=[
                "Low",
                "Medium",
                "High",
                "Very High",
            ],
        )

        product_features = (
            product_features.rename(
                columns={
                    "Description": "Product_Name",
                }
            )
        )

        # Final protection against whitespace in
        # product names and stock codes.
        product_features[
            "StockCode"
        ] = (
            product_features[
                "StockCode"
            ]
            .astype("string")
            .str.strip()
        )

        product_features[
            "Product_Name"
        ] = (
            product_features[
                "Product_Name"
            ]
            .astype("string")
            .str.strip()
        )

        self.products = product_features

        # ----------------------------------------------------
        # Order analytics
        # ----------------------------------------------------

        order_features = (
            df.groupby("Invoice")
            .agg(
                Order_Revenue=(
                    "Revenue",
                    "sum",
                ),
                Units=(
                    "Quantity",
                    "sum",
                ),
                Unique_Products=(
                    "StockCode",
                    "nunique",
                ),
                Customer_ID=(
                    "Customer ID",
                    "first",
                ),
                Country=(
                    "Country",
                    "first",
                ),
                Order_Date=(
                    "InvoiceDate",
                    "first",
                ),
            )
            .reset_index()
        )

        order_features[
            "Average_Item_Value"
        ] = (
            order_features[
                "Order_Revenue"
            ]
            / order_features[
                "Units"
            ].replace(0, pd.NA)
        )

        order_features[
            "Basket_Size"
        ] = order_features[
            "Unique_Products"
        ]

        self.orders = order_features

        # ----------------------------------------------------
        # Store active dataset
        # ----------------------------------------------------

        self.transactions = df
        self.dataset_name = dataset_name

        return {
            "rows": len(df),
            "customers": len(self.customers),
            "products": len(self.products),
            "orders": len(self.orders),
            "revenue": float(
                df["Revenue"].sum()
            ),
            "dataset_name": dataset_name,
        }


dataset_manager = DatasetManager()

