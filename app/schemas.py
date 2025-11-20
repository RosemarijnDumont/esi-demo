from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TicketBase(BaseModel):
    subject: str
    status: str
    submission_date: datetime
    last_update: datetime
    assigned_agent: str

class TicketCreate(TicketBase):
    user_id: str

class Ticket(TicketBase):
    ticket_id: str
    user_id: str

    class Config:
        from_attributes = True
