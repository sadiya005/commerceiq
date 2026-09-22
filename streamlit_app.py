import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


st.set_page_config(
    page_title="CommerceIQ",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)


API_URL = os.getenv(
    "COMMERCEIQ_API_URL",
    "http://16.171.32.175:8000",
).rstrip("/")


st.markdown(
    """
    <style>
        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        /* Main hero */
        .hero {
            padding: 1.6rem 1.8rem;
            border-radius: 16px;
            background: linear-gradient(
                135deg,
                rgba(49, 51, 63, 0.95),
                rgba(28, 30, 38, 0.95)
            );
            margin-bottom: 1.5rem;
        }

        .hero h1 {
            margin-bottom: 0.25rem;
            font-size: 2.4rem;
            color: #ffffff !important;
        }

        .hero p {
            margin-top: 0;
            color: #d6d7df !important;
            font-size: 1.05rem;
        }

        /* AI answer box */
        .answer-box {
            padding: 1.2rem;
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.30);
            background: #f4f4f6;
            color: #18181b !important;
            font-size: 1rem;
            line-height: 1.6;
        }

        .answer-box * {
            color: #18181b !important;
        }

        /* Tool chips */
        .tool-chip {
            display: inline-block;
            padding: 0.35rem 0.65rem;
            margin: 0.15rem;
            border-radius: 999px;
            background: #31333f;
            border: 1px solid rgba(128, 128, 128, 0.35);
            color: #ffffff !important;
            font-size: 0.85rem;
        }

        /* API status */
        .status-good {
            color: #4ade80 !important;
            font-weight: 600;
        }

        /*
        Make text inside Streamlit alert boxes readable.
        These include st.info, st.success, st.warning and st.error.
        */

        [data-testid="stAlert"] {
            color: #18181b !important;
        }

        [data-testid="stAlert"] p {
            color: #18181b !important;
        }

        [data-testid="stAlert"] strong {
            color: #111111 !important;
        }

        [data-testid="stAlert"] div {
            color: #18181b !important;
        }

        [data-testid="stAlert"] span {
            color: #18181b !important;
        }

        /* Keep buttons readable */
        .stButton button {
            font-weight: 600;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.18);
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def api_get(endpoint, params=None, timeout=30):
    try:
        response = requests.get(
            f"{API_URL}{endpoint}",
            params=params,
            timeout=timeout,
        )

        if response.status_code == 404:
            return None, f"Resource not found: {endpoint}"

        response.raise_for_status()

        return response.json(), None

    except requests.exceptions.RequestException as exc:
        return None, str(exc)


def api_post(endpoint, payload, timeout=120):
    try:
        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=timeout,
        )

        response.raise_for_status()

        return response.json(), None

    except requests.exceptions.RequestException as exc:
        return None, str(exc)


def api_upload(endpoint, uploaded_file, timeout=120):
    try:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "text/csv",
            )
        }

        response = requests.post(
            f"{API_URL}{endpoint}",
            files=files,
            timeout=timeout,
        )

        response.raise_for_status()

        return response.json(), None

    except requests.exceptions.HTTPError as exc:
        try:
            detail = response.json().get(
                "detail",
                str(exc),
            )
        except Exception:
            detail = str(exc)

        return None, detail

    except requests.exceptions.RequestException as exc:
        return None, str(exc)


@st.cache_data(ttl=60)
def get_revenue():
    return api_get("/revenue")


@st.cache_data(ttl=60)
def get_top_products(top_k=5):
    return api_get(
        "/top-products",
        params={"top_k": top_k},
    )


@st.cache_data(ttl=60)
def get_customer(customer_id):
    return api_get(
        f"/customer/{customer_id}"
    )


@st.cache_data(ttl=60)
def get_product(stock_code):
    return api_get(
        f"/product/{stock_code}"
    )


@st.cache_data(ttl=30)
def get_health():
    return api_get("/health")


st.sidebar.title("🛒 CommerceIQ")

st.sidebar.caption(
    "E-commerce analytics powered by AI"
)

st.sidebar.divider()


page = st.sidebar.radio(
    "Navigation",
    [
        "📂 Upload Data",
        "🏠 Overview",
        "🤖 AI Analyst",
        "👤 Customer Explorer",
        "🛍️ Product Explorer",
        "📊 Product Analytics",
    ],
)


st.sidebar.divider()


health_data, health_error = get_health()


if health_data and health_data.get("status") == "healthy":
    st.sidebar.markdown(
        '<span class="status-good">● API Online</span>',
        unsafe_allow_html=True,
    )
else:
    st.sidebar.error("● API Offline")


# Main page title
st.markdown(
    """
    <div class="hero">
        <h1>🛒 CommerceIQ</h1>
        <p>
            Turn e-commerce data into actionable business insights
            with analytics and AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


if page == "📂 Upload Data":

    st.subheader("📂 Upload E-commerce Data")

    st.write(
        "Upload a compatible e-commerce CSV to replace the "
        "currently active dataset for analytics and AI analysis."
    )

    st.info(
        "CSV files only. The uploaded dataset is kept in memory "
        "and is not permanently stored by CommerceIQ."
    )

    st.subheader("Required columns")

    required_columns = [
        "Invoice",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "Price",
        "Customer ID",
        "Country",
    ]

    st.code(", ".join(required_columns))

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help=(
            "The CSV must contain all required e-commerce "
            "transaction columns."
        ),
    )

    if uploaded_file is not None:

        st.write(
            f"Selected file: **{uploaded_file.name}**"
        )

        try:
            preview_df = pd.read_csv(uploaded_file)

            st.subheader("Dataset Preview")

            st.dataframe(
                preview_df.head(10),
                hide_index=True,
                use_container_width=True,
            )

            missing_columns = [
                column
                for column in required_columns
                if column not in preview_df.columns
            ]

            if missing_columns:

                st.error(
                    "Missing required columns: "
                    + ", ".join(missing_columns)
                )

            else:

                st.success(
                    "Dataset structure is compatible."
                )

                if st.button(
                    "Upload and Process Dataset",
                    type="primary",
                    use_container_width=True,
                ):

                    with st.spinner(
                        "Uploading and processing dataset..."
                    ):

                        result, error = api_upload(
                            "/upload-dataset",
                            uploaded_file,
                        )

                    if error:

                        st.error(
                            f"Dataset upload failed: {error}"
                        )

                    else:

                        dataset = result.get(
                            "dataset",
                            {},
                        )

                        st.success(
                            result.get(
                                "message",
                                "Dataset uploaded successfully.",
                            )
                        )

                        st.subheader("Active Dataset")

                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric(
                                "Rows",
                                f"{dataset.get('rows', 0):,}",
                            )

                        with col2:
                            st.metric(
                                "Customers",
                                f"{dataset.get('customers', 0):,}",
                            )

                        with col3:
                            st.metric(
                                "Products",
                                f"{dataset.get('products', 0):,}",
                            )

                        with col4:
                            st.metric(
                                "Orders",
                                f"{dataset.get('orders', 0):,}",
                            )

                        st.metric(
                            "Revenue",
                            f"£{dataset.get('revenue', 0):,.2f}",
                        )

                        st.caption(
                            f"Active dataset: "
                            f"{dataset.get('dataset_name', uploaded_file.name)}"
                        )

                        get_revenue.clear()
                        get_top_products.clear()
                        get_customer.clear()
                        get_product.clear()
                        get_health.clear()

                        st.session_state[
                            "dataset_uploaded"
                        ] = True

                        st.info(
                            "The new dataset is now active. "
                            "Navigate to Overview, Customer Explorer, "
                            "Product Explorer, Product Analytics, or "
                            "AI Analyst to work with it."
                        )

        except Exception as exc:

            st.error(
                f"Could not read the CSV file: {exc}"
            )


elif page == "🏠 Overview":

    st.subheader("Business Overview")

    st.info(
            "**Demo Dataset Active**\n\n"
            "CommerceIQ includes a preloaded e-commerce dataset so you "
            "can explore the platform immediately. Upload your own "
            "compatible CSV from **Upload Data** to analyze a different "
            "dataset."
        )

    revenue_data, revenue_error = get_revenue()

    if revenue_error:

        st.error(
            f"Could not load business data: {revenue_error}"
        )

        st.stop()

    total_revenue = revenue_data["total_revenue"]
    total_products = revenue_data["total_products"]
    total_customers = revenue_data["total_customers"]
    total_orders = revenue_data["total_orders"]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Revenue",
            f"£{total_revenue:,.2f}",
        )

    with col2:
        st.metric(
            "Orders",
            f"{total_orders:,}",
        )

    with col3:
        st.metric(
            "Customers",
            f"{total_customers:,}",
        )

    with col4:
        st.metric(
            "Products",
            f"{total_products:,}",
        )

    st.divider()

    top_data, top_error = get_top_products(5)

    if top_error:

        st.error(top_error)

    else:

        products = top_data.get(
            "products",
            [],
        )

        if products:

            df = pd.DataFrame(products)

            st.subheader("Top Revenue Products")

            chart = px.bar(
                df.sort_values("total_revenue"),
                x="total_revenue",
                y="product_name",
                orientation="h",
                labels={
                    "total_revenue": "Revenue (£)",
                    "product_name": "Product",
                },
            )

            chart.update_layout(
                height=430,
                margin=dict(
                    l=10,
                    r=10,
                    t=20,
                    b=10,
                ),
            )

            st.plotly_chart(
                chart,
                use_container_width=True,
            )

    st.divider()

    st.subheader("Explore CommerceIQ")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "**AI Analyst**\n\n"
            "Ask natural-language questions about "
            "your e-commerce business."
        )

    with col2:
        st.info(
            "**Customer Explorer**\n\n"
            "Investigate customer revenue, orders, "
            "products and segments."
        )

    with col3:
        st.info(
            "**Product Explorer**\n\n"
            "Analyze product revenue, units, orders "
            "and customer reach."
        )


elif page == "🤖 AI Analyst":

    st.subheader("🤖 AI Analyst")

    st.write(
        "Ask CommerceIQ questions about customers, "
        "products and business performance."
    )

    example_questions = [
        "What is the total CommerceIQ revenue?",
        "Compare customer 12346's revenue with the overall CommerceIQ revenue.",
        "Tell me about product 10002.",
        "What are the top revenue-generating products?",
        "What information is available for customer 12346?",
    ]

    selected_example = st.selectbox(
        "Try an example",
        ["Custom question"] + example_questions,
    )

    if selected_example == "Custom question":
        default_question = ""
    else:
        default_question = selected_example

    question = st.text_area(
        "Ask a question",
        value=default_question,
        height=110,
        placeholder="e.g. Which products generate the most revenue?",
    )

    if st.button(
        "Ask CommerceIQ",
        type="primary",
        use_container_width=True,
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

            st.stop()

        with st.spinner(
            "Analyzing CommerceIQ data..."
        ):

            result, error = api_post(
                "/ask",
                {"question": question},
            )

        if error:

            st.error(
                f"API request failed: {error}"
            )

        else:

            st.subheader("Answer")

            st.markdown(
                f"""
                <div class="answer-box">
                {result.get(
                    "answer",
                    "No answer returned."
                )}
                </div>
                """,
                unsafe_allow_html=True,
            )

            tool_calls = result.get(
                "tool_calls",
                [],
            )

            if tool_calls:

                st.caption(
                    "Evidence retrieved using:"
                )

                for call in tool_calls:

                    tool_name = call.get(
                        "tool",
                        "unknown",
                    )

                    st.markdown(
                        f"""
                        <span class="tool-chip">
                        ✓ {tool_name}
                        </span>
                        """,
                        unsafe_allow_html=True,
                    )


elif page == "👤 Customer Explorer":

    st.subheader("👤 Customer Explorer")

    customer_id = st.number_input(
        "Customer ID",
        min_value=1,
        value=12346,
        step=1,
    )

    if st.button(
        "Lookup Customer",
        type="primary",
    ):

        with st.spinner(
            "Loading customer..."
        ):

            customer, error = get_customer(
                int(customer_id)
            )

        if error:

            st.error(
                f"Customer lookup failed: {error}"
            )

        elif customer:

            if customer.get("status") != "success":

                st.warning(
                    customer.get(
                        "message",
                        "Customer not found.",
                    )
                )

                st.stop()

            st.success(
                f"Customer {customer['customer_id']} found."
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Revenue",
                    f"£{customer['total_revenue']:,.2f}",
                )

            with col2:
                st.metric(
                    "Orders",
                    f"{customer['total_orders']:,}",
                )

            with col3:
                st.metric(
                    "Units",
                    f"{customer['total_units']:,}",
                )

            with col4:
                st.metric(
                    "Products",
                    f"{customer['unique_products']:,}",
                )

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Average Order Value",
                    f"£{customer['average_order_value']:,.2f}",
                )

            with col2:
                st.metric(
                    "Revenue Segment",
                    customer["revenue_segment"],
                )

            with col3:
                st.metric(
                    "Activity Segment",
                    customer["activity_segment"],
                )

            st.divider()

            st.subheader("Customer Details")

            profile = pd.DataFrame(
                {
                    "Metric": [
                        "Customer ID",
                        "Total Orders",
                        "Total Revenue",
                        "Total Units",
                        "Unique Products",
                        "Recency",
                    ],
                    "Value": [
                        customer["customer_id"],
                        customer["total_orders"],
                        f"£{customer['total_revenue']:,.2f}",
                        customer["total_units"],
                        customer["unique_products"],
                        f"{customer['recency_days']} days",
                    ],
                }
            )

            st.dataframe(
                profile,
                hide_index=True,
                use_container_width=True,
            )


elif page == "🛍️ Product Explorer":

    st.subheader("🛍️ Product Explorer")

    stock_code = st.text_input(
        "Stock Code",
        value="10002",
    )

    if st.button(
        "Lookup Product",
        type="primary",
    ):

        if not stock_code.strip():

            st.warning(
                "Enter a stock code."
            )

            st.stop()

        with st.spinner(
            "Loading product..."
        ):

            product, error = get_product(
                stock_code.strip()
            )

        if error:

            st.error(
                f"Product lookup failed: {error}"
            )

        elif product:

            if product.get("status") != "success":

                st.warning(
                    product.get(
                        "message",
                        "Product not found.",
                    )
                )

                st.stop()

            st.success(
                f"Product {product['stock_code']} found."
            )

            st.subheader(
                product["product_name"]
            )

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    "Revenue",
                    f"£{product['total_revenue']:,.2f}",
                )

            with col2:
                st.metric(
                    "Units Sold",
                    f"{product['total_units_sold']:,}",
                )

            with col3:
                st.metric(
                    "Orders",
                    f"{product['orders']:,}",
                )

            with col4:
                st.metric(
                    "Customers",
                    f"{product['customers']:,}",
                )

            st.divider()

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Average Price",
                    f"£{product['average_price']:.2f}",
                )

            with col2:
                st.metric(
                    "Customer Reach",
                    f"{product['customer_penetration'] * 100:.2f}%",
                )

            with col3:
                st.metric(
                    "Revenue Segment",
                    product["revenue_segment"],
                )


elif page == "📊 Product Analytics":

    st.subheader("📊 Product Analytics")

    top_k = st.slider(
        "Products to display",
        min_value=3,
        max_value=20,
        value=10,
    )

    data, error = get_top_products(top_k)

    if error:

        st.error(error)

    else:

        products = data.get(
            "products",
            [],
        )

        if not products:

            st.info(
                "No product data returned."
            )

            st.stop()

        df = pd.DataFrame(products)

        chart = px.bar(
            df.sort_values("total_revenue"),
            x="total_revenue",
            y="product_name",
            orientation="h",
            labels={
                "total_revenue": "Revenue (£)",
                "product_name": "Product",
            },
            title=f"Top {top_k} Products by Revenue",
        )

        chart.update_layout(
            height=max(
                450,
                top_k * 45,
            ),
            margin=dict(
                l=10,
                r=10,
                t=50,
                b=10,
            ),
        )

        st.plotly_chart(
            chart,
            use_container_width=True,
        )

        st.subheader(
            "Product Performance"
        )

        display_columns = [
            "stock_code",
            "product_name",
            "total_revenue",
            "total_units_sold",
            "orders",
            "customers",
        ]

        available_columns = [
            column
            for column in display_columns
            if column in df.columns
        ]

        display_df = df[
            available_columns
        ].copy()

        if "total_revenue" in display_df.columns:

            display_df["total_revenue"] = (
                display_df["total_revenue"]
                .map(
                    lambda x: f"£{x:,.2f}"
                )
            )

        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
        )


st.divider()

st.caption(
    "CommerceIQ • E-commerce Analytics + AI"
)