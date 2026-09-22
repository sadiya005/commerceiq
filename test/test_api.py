from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "CommerceIQ API"


def test_customer_endpoint():
    response = client.get("/customer/12346")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["customer_id"] == 12346
    assert data["total_revenue"] == 77183.6


def test_invalid_customer_endpoint():
    response = client.get("/customer/999999")

    assert response.status_code == 404


def test_product_endpoint():
    response = client.get("/product/10002")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert data["stock_code"] == "10002"
    assert data["product_name"] == "INFLATABLE POLITICAL GLOBE"
    assert data["total_revenue"] == 759.89


def test_revenue_endpoint():
    response = client.get("/revenue")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert round(data["total_revenue"], 2) == 10539552.83
    assert data["total_products"] == 3918
    assert data["total_customers"] == 4335
    assert data["total_orders"] == 19865


def test_top_products_endpoint():
    response = client.get("/top-products")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert len(data["products"]) == 5

    assert data["products"][0]["stock_code"] == "22423"
    assert data["products"][1]["stock_code"] == "23843"
    assert data["products"][2]["stock_code"] == "85123A"


def test_top_products_custom_k():
    response = client.get("/top-products?top_k=3")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert len(data["products"]) == 3


def test_top_products_invalid_k():
    response = client.get("/top-products?top_k=50")

    assert response.status_code == 400


def test_ask_endpoint():
    response = client.post(
        "/ask",
        json={
            "question": "Compare customer 12346's revenue with the overall CommerceIQ revenue."
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "answer" in data
    assert "tool_calls" in data

    assert len(data["tool_calls"]) >= 1


def test_ask_empty_question():
    response = client.post(
        "/ask",
        json={
            "question": ""
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Question cannot be empty."