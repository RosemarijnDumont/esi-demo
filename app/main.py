from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import List, Dict
from datetime import datetime

app = FastAPI(title="Self-Service Ticket Status Dashboard API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# This is a placeholder for a real database connection and ORM
# In a production environment, you would use SQLAlchemy, Tortoise ORM, etc.
class MockServiceDeskDB:
    def __init__(self):
        self.tickets = {
            "user1": [
                {
                    "ticket_id": "T1001",
                    "user_id": "user1",
                    "subject": "My laptop is not turning on",
                    "status": "Open",
                    "submission_date": datetime(2023, 1, 10, 10, 0, 0),
                    "last_update": datetime(2023, 1, 12, 14, 30, 0),
                    "assigned_agent": "Alice Smith",
                },
                {
                    "ticket_id": "T1002",
                    "user_id": "user1",
                    "subject": "Difficulty accessing shared drive",
                    "status": "Pending",
                    "submission_date": datetime(2023, 1, 15, 9, 0, 0),
                    "last_update": datetime(2023, 1, 15, 11, 0, 0),
                    "assigned_agent": "Bob Johnson",
                },
                {
                    "ticket_id": "T1003",
                    "user_id": "user1",
                    "subject": "Password reset request",
                    "status": "Closed",
                    "submission_date": datetime(2023, 1, 5, 16, 0, 0),
                    "last_update": datetime(2023, 1, 6, 9, 0, 0),
                    "assigned_agent": "Alice Smith",
                },
            ],
            "user2": [
                {
                    "ticket_id": "T2001",
                    "user_id": "user2",
                    "subject": "Request for new software installation",
                    "status": "Open",
                    "submission_date": datetime(2023, 2, 1, 11, 0, 0),
                    "last_update": datetime(2023, 2, 2, 10, 0, 0),
                    "assigned_agent": "Charlie Brown",
                },
            ],
        }

    def get_tickets_by_user(self, user_id: str) -> List[Dict]:
        return self.tickets.get(user_id, [])

    def get_ticket_by_id(self, user_id: str, ticket_id: str) -> Dict | None:
        for ticket in self.tickets.get(user_id, []):
            if ticket["ticket_id"] == ticket_id:
                return ticket
        return None


mock_db = MockServiceDeskDB()

# Placeholder for a real authentication/authorization system
# In a production environment, you would validate JWT tokens against a real IdP
async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    # Here we simulate user extraction from a token. In a real scenario,
    # you would decode the JWT token and get the user ID.
    # For this example, let's assume the token itself specifies the user (e.g., "user1-token").
    if token == "user1-token":
        return "user1"
    elif token == "user2-token":
        return "user2"
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/tickets", response_model=List[Dict], summary="Retrieve all open tickets for the authenticated user")
async def get_user_tickets(current_user: str = Depends(get_current_user)):
    """
    Retrieve a list of all open tickets associated with the authenticated user.
    """
    tickets = mock_db.get_tickets_by_user(current_user)
    # Filter for open tickets. In a real scenario, this filtering would ideally happen at the DB layer.
    open_tickets = [ticket for ticket in tickets if ticket["status"].lower() != "closed"]
    return open_tickets

@app.get("/tickets/{ticket_id}", response_model=Dict, summary="Retrieve details for a specific ticket")
async def get_ticket_details(ticket_id: str, current_user: str = Depends(get_current_user)):
    """
    Retrieve detailed information for a specific ticket by its ID,
    ensuring the ticket belongs to the authenticated user.
    """
    ticket = mock_db.get_ticket_by_id(current_user, ticket_id)
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found or unauthorized")
    return ticket


# Example of how you might run this using uvicorn:
# uvicorn main:app --reload --port 8000
