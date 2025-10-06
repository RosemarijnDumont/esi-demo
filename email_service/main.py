import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class EmailRequest(BaseModel):
    customer_id: str
    inquiry_type: str
    details: dict = {}

@app.post("/process_email/")
async def process_email(request: EmailRequest):
    # Here, you'd implement the logic for:
    # 1. Matching inquiry_type to defined triggers/rules
    # 2. Retrieving customer data using customer_id (via API endpoint)
    # 3. Generating dynamic email content using a templating engine
    # 4. Sending the email
    print(f"Received email request for customer {request.customer_id} of type {request.inquiry_type}")
    # Placeholder for actual processing logic
    return {"status": "Email processing initiated", "customer_id": request.customer_id, "inquiry_type": request.inquiry_type}

@app.get("/customer_data/{customer_id}/")
async def get_customer_data(customer_id: str):
    # Placeholder for fetching real customer data from a database or CRM
    print(f"Fetching data for customer {customer_id}")
    if customer_id == "123":
        return {"customer_id": "123", "name": "John Doe", "email": "john.doe@example.com", "orders": [{"order_id": "ABC", "status": "shipped"}]}
    return {"customer_id": customer_id, "name": "Unknown", "email": "unknown@example.com", "orders": []}

# To run the service:
# uvicorn main:app --reload --port 8001
