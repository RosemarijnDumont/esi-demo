
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas, database, auth

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    models.Base.metadata.create_all(bind=database.engine)

@app.get("/user/preferences/{user_id}", response_model=schemas.n_app_preferences)
def get_user_preferences(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
    ):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view these preferences")
    db_preferences = crud.get_user_preferences(db, user_id=user_id)
    if db_preferences is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User preferences not found")
    return db_preferences

@app.put("/user/preferences/{user_id}", response_model=schemas.n_app_preferences)
def update_user_preferences(
    user_id: int, 
    preferences: schemas.NotificationPreferenceUpdate, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
    ):
    if user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update these preferences")
    db_preferences = crud.get_user_preferences(db, user_id=user_id)
    if db_preferences is None:
        # If preferences don't exist, create them
        return crud.create_user_preferences(db=db, user_id=user_id, preferences=preferences)
    return crud.update_user_preferences(db=db, user_id=user_id, preferences=preferences)

