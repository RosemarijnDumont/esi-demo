
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
import datetime

from . import models, schemas, crud
from .database import SessionLocal, engine
from .kafka_producer import send_notification_to_kafka
from .third_party_services import send_email_with_provider

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notification Service",
    description="Microservice for orchestrating, generating, and sending notifications (email and in-app).",
    version="1.0.0",
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/notifications/send", response_model=schemas.NotificationResponse)
async def trigger_notification(notification_request: schemas.NotificationCreate, db: Session = Depends(get_db)):
    """
    Triggers a notification to be sent. This endpoint enqueues the notification for asynchronous processing.
    """
    try:
        notification_data = notification_request.dict()
        enqueued_notification = crud.create_notification_log(db, notification_data)
        await send_notification_to_kafka(enqueued_notification.id, notification_request.notification_type, notification_request.recipient, notification_request.template_name, notification_request.template_data)
        return schemas.NotificationResponse(message="Notification enqueued successfully", notification_id=enqueued_notification.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to enqueue notification: {str(e)}")

@app.get("/notifications/{notification_id}", response_model=schemas.NotificationLog)
def get_notification_status(notification_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the status of a sent notification.
    """
    notification = crud.get_notification_log(db, notification_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@app.post("/notification-preferences/", response_model=schemas.UserPreferences)
def create_user_preferences(preferences: schemas.UserPreferencesCreate, db: Session = Depends(get_db)):
    """
    Creates new notification preferences for a user.
    """
    db_preferences = crud.get_user_preferences(db, preferences.user_id)
    if db_preferences:
        raise HTTPException(status_code=400, detail="User preferences already exist. Use PUT to update.")
    return crud.create_user_preferences(db, preferences)

@app.get("/notification-preferences/{user_id}", response_model=schemas.UserPreferences)
def get_user_preferences(user_id: int, db: Session = Depends(get_db)):\n    """
    Retrieves notification preferences for a specific user.\n    """
    preferences = crud.get_user_preferences(db, user_id)\n    if preferences is None:\n        raise HTTPException(status_code=404, detail="User preferences not found")\n    return preferences\n\n@app.put("/notification-preferences/{user_id}", response_model=schemas.UserPreferences)\ndef update_user_preferences(user_id: int, preferences: schemas.UserPreferencesUpdate, db: Session = Depends(get_db)):\n    """\n    Updates existing notification preferences for a user.\n    """\n    db_preferences = crud.get_user_preferences(db, user_id)\n    if db_preferences is None:\n        raise HTTPException(status_code=404, detail="User preferences not found")\n    return crud.update_user_preferences(db, user_id, preferences)\n\n@app.delete("/notification-preferences/{user_id}", status_code=204)\ndef delete_user_preferences(user_id: int, db: Session = Depends(get_db)):\n    """\n    Deletes notification preferences for a user.\n    """\n    db_preferences = crud.get_user_preferences(db, user_id)\n    if db_preferences is None:\n        raise HTTPException(status_code=404, detail="User preferences not found")\n    crud.delete_user_preferences(db, user_id)\n    return # No content on successful deletion\n\n# --- Internal Endpoints (for worker/consumer) ---\n@app.post("/_internal/notifications/process", response_model=schemas.NotificationResponse)\nasync def process_notification_internal(notification_process_request: schemas.NotificationProcessRequest, db: Session = Depends(get_db)):\n    """\n    Internal endpoint for notification worker to update status and handle retries.\n    Not directly exposed to external services.\n    """\n    log_entry = crud.get_notification_log(db, notification_process_request.notification_id)\n    if not log_entry:\n        raise HTTPException(status_code=404, detail="Notification log entry not found")\n\n    log_entry = crud.update_notification_log_status(db, notification_process_request.notification_id, notification_process_request.status, notification_process_request.details)\n    \n    if notification_process_request.status == "failed" and notification_process_request.retries_attempted < 3: # Example retry limit\n        # Re-enqueue for retry after a delay\n        print(f"Retrying notification {notification_process_request.notification_id}, attempt {notification_process_request.retries_attempted + 1}")\n        await send_notification_to_kafka(\n            notification_process_request.notification_id,\n            log_entry.notification_type,\n            log_entry.recipient,\n            log_entry.template_name,\n            log_entry.template_data,\n            retries_attempted=notification_process_request.retries_attempted + 1\n        )\n    return schemas.NotificationResponse(message="Notification processed internally.", notification_id=log_entry.id)