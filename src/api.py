from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pandas as pd

from src.data_loader import load_all_data
from src.analytics import (
    lookup_customer,
    lookup_product,
    revenue_summary,
    top_revenue_products,
)
from src.agent import commerceiq_agent
from src.dataset_manager import dataset_manager


# ============================================================
# DEFAULT DATASET
# ============================================================

customer_data, product_data, order_data = load_all_data()

# Clean the default precomputed analytics before making them
# the active dataset.
customer_data = customer_data.copy()
product_data = product_data.copy()
order_data = order_data.copy()

if "Product_Name" in product_data.columns:
    product_data["Product_Name"] = (
        product_data["Product_Name"]
        .astype("string")
        .str.strip()
    )

if "StockCode" in product_data.columns:
    product_data["StockCode"] = (
        product_data["StockCode"]
        .astype("string")
        .str.strip()
    )

dataset_manager.customers = customer_data
dataset_manager.products = product_data
dataset_manager.orders = order_data


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CommerceIQ API",
    description=(
        "Production API for the CommerceIQ "
        "e-commerce analytics and AI system."
    ),
    version="1.0.0",
)


class AskRequest(BaseModel):
    question: str


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CommerceIQ API",
    }


# ============================================================
# CUSTOMER
# ============================================================

@app.get("/customer/{customer_id}")
def get_customer(customer_id: int):

    result = lookup_customer(customer_id)

    if result["status"] != "success":
        raise HTTPException(
            status_code=404,
            detail=result["message"],
        )

    return result


# ============================================================
# PRODUCT
# ============================================================

@app.get("/product/{stock_code}")
def get_product(stock_code: str):

    result = lookup_product(stock_code)

    if result["status"] != "success":
        raise HTTPException(
            status_code=404,
            detail=result["message"],
        )

    return result


# ============================================================
# REVENUE
# ============================================================

@app.get("/revenue")
def get_revenue():
    return revenue_summary()


# ============================================================
# TOP PRODUCTS
# ============================================================

@app.get("/top-products")
def get_top_products(top_k: int = 5):

    if top_k < 1 or top_k > 20:
        raise HTTPException(
            status_code=400,
            detail="top_k must be between 1 and 20.",
        )

    return top_revenue_products(top_k=top_k)


# ============================================================
# AI ANALYST
# ============================================================

@app.post("/ask")
def ask_commerceiq(request: AskRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    return commerceiq_agent(request.question)


# ============================================================
# DATASET UPLOAD
# ============================================================

@app.post("/upload-dataset")
async def upload_dataset(
    file: UploadFile = File(...),
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file provided.",
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are currently supported.",
        )

    try:

        contents = await file.read()

        from io import BytesIO

        df = pd.read_csv(
            BytesIO(contents)
        )

        result = dataset_manager.load_dataset(
            df,
            dataset_name=file.filename,
        )

        return {
            "status": "success",
            "message": (
                "Dataset uploaded and processed successfully."
            ),
            "dataset": result,
        }

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Dataset processing failed: {exc}",
        )