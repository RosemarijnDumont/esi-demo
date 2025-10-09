import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the ML6 Food Ordering API!"}

def test_submit_order():
    order_data = {
        "items": [
            {"item_id": 1, "quantity": 2},
            {"item_id": 2, "quantity": 1}
        ],
        "location": "Office A",
        "user_id": "test_user_123"
    }
    response = client.post("/order", json=order_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Order submitted successfully!", "order": order_data}

def test_submit_order_invalid_data():
    # Missing 'items' field
    order_data_invalid = {
        "location": "Office B",
        "user_id": "test_user_456"
    }
    response = client.post("/order", json=order_data_invalid)
    assert response.status_code == 422 # Unprocessable Entity for Pydantic validation error

    # Invalid quantity type
    order_data_invalid_quantity = {
        "items": [
            {"item_id": 1, "quantity": "invalid"}
        ],
        "location": "Office C",
        "user_id": "test_user_789"
    }
    response = client.post("/order", json=order_data_invalid_quantity)
    assert response.status_code == 422


def test_integration_full_order_process():
    # This test simulates a full end-to-end order process

    # 1. Get available food items (assuming an endpoint exists or mock data)
    # For simplicity, we'll use predefined food items here.
    food_items = [
        {"id": 1, "name": "Pizza", "price": 10},
        {"id": 2, "name": "Burger", "price": 8}
    ]

    # 2. Simulate user selecting items and location
    selected_order = {
        "items": [
            {"item_id": food_items[0]["id"], "quantity": 3},
            {"item_id": food_items[1]["id"], "quantity": 1}
        ],
        "location": "Office C",
        "user_id": "integration_test_user"
    }

    # 3. Submit the order to the backend
    response = client.post("/order", json=selected_order)
    assert response.status_code == 200
    assert response.json() == {"message": "Order submitted successfully!", "order": selected_order}

    # 4. (Optional) In a real scenario, you might add steps here to:
    #    - Verify the order was recorded in a database.
    #    - Check if a notification was sent to the vendor.
    #    - Simulate a confirmation being sent to the user.

    # For this integration test, we'll consider the successful API response as confirmation
    print("Integration Test: Order submitted and confirmed successfully!")