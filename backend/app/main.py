from fastapi import FastAPI
from backend.app.api.endpoints import email_automation
from backend.app.db.base import Base
from backend.app.db.session import engine

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automated Emails API",
    description="API for managing automated email rules, templates, and triggers for support processes.",
    version="1.0.0",
)

app.include_router(email_automation.router, prefix="/email-automation", tags=["email-automation"])

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Automated Emails API"}
