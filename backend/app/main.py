# main.py
from fastapi import FastAPI, HTTPException
from typing import List, Dict
from pydantic import BaseModel

app = FastAPI()

# In-memory storage for locations and orders (replace with a database in production)
ml6_locations = {
    "main_office": {"name": "ML6 Main Office", "address": "Some Street 1, Ghent"},
    "annex_b": {"name": "ML6 Annex B", "address": "Another Street 10, Ghent"},
}

class OrderItem(BaseModel):
    item_name: str
    quantity: int

class Order(BaseModel):
    customer_name: str
    location_id: str
    items: List[OrderItem]
    notes: str = None

# Placeholder for a vendor notification system (e.g., email, webhook)
def notify_vendor(order: Order):
    print(f"Notifying vendor for order: {order.dict()}")
    # In a real application, this would send an email, call a webhook, etc.
    pass

@app.get("/locations", response_model=Dict)
async def get_locations():
    return ml6_locations

@app.post("/orders")
async def create_order(order: Order):
    if order.location_id not in ml6_locations:
        raise HTTPException(status_code=400, detail="Invalid location ID")
    
    # Basic order validation (e.g., check for positive quantities)
    for item in order.items:
        if item.quantity <= 0:
            raise HTTPException(status_code=400, detail=f"Quantity for {item.item_name} must be positive")

    # In a real application, save the order to a database
    # For this example, we'll just 