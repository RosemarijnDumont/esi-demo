# test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_locations():
    response = client.get("/locations")
    assert response.status_code == 200
    assert "main_office" in response.json()
    assert "annex_b" in response.json()

def test_create_order_success():
    order_data = {
        "customer_name": "John Doe",
        "location_id": "main_office",
        "items": [
            {"item_name": "Pizza", "quantity": 2},
            {"item_name": "Coke", "quantity": 4}
        ],
        "notes": "Extra cheese on pizza"
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 200
    assert "Order submitted successfully" in response.json()["message"]

def test_create_order_invalid_location():
    order_data = {
        "customer_name": "Jane Doe",
        "location_id": "non_existent_office",
        "items": [
            {"item_name": "Salad", "quantity": 1}
        ]
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 400
    assert "Invalid location ID" in response.json()["detail"]

def test_create_order_invalid_quantity():
    order_data = {
        "customer_name": "Peter Smith",
        "location_id": "main_office",
        "items": [
            {"item_name": "Burger", "quantity": 0}
        ]
    }
    response = client.post("/orders", json=order_data)
    assert response.status_code == 400
    assert "Quantity for Burger must be positive" in response.json()["detail"]
