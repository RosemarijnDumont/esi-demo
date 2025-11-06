
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class FinancialTransaction(BaseModel):
    id: int
    transaction_date: datetime
    amount: float = Field(..., gt=0, description="Amount must be a positive number.")
    currency: str = Field(..., max_length=3)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[str] = Field(None, max_length=100) # Assuming category name here for simplicity
    account_id: int
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "transaction_date": "2023-01-15T10:00:00Z",
                "amount": 123.45,
                "currency": "USD",
                "description": "Payment for services",
                "category": "Income",
                "account_id": 101,
                "created_at": "2023-01-15T09:00:00Z",
                "updated_at": "2023-01-15T10:00:00Z",
                "metadata": {"invoice_id": "INV001"}
            }
        }

