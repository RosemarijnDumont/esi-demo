from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for idea submission
class IdeaCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    submitter_name: str = Field(..., min_length=1, max_length=255)
    submitter_email: str = Field(..., regex="^[\w\.-]+@[\w\.-]+\.\w+$")

@app.post("/api/ideas", status_code=201)
async def submit_idea(idea: IdeaCreate, db: Session = Depends(get_db)):
    """
    Submit a new idea to the intranet.

    This endpoint receives an idea submission, validates the data, and stores it in the database.
    """
    try:
        db_idea = models.Idea(
            title=idea.title,
            description=idea.description,
            submitter_name=idea.submitter_name,
            submitter_email=idea.submitter_email,
            submission_timestamp=datetime.now()
        )
        db.add(db_idea)
        db.commit()
        db.refresh(db_idea)
        return {"message": "Idea submitted successfully!", "id": db_idea.id}
    except Exception as e:
        db.rollback()
        import logging
        logging.error(f"Error submitting idea: {e}")
        raise HTTPException(status_code=500, detail="Internal server error. Could not submit idea.")

