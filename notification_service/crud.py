
from sqlalchemy.orm import Session
from . import models, schemas

def create_notification_log(db: Session, notification: dict):
    db_notification = models.NotificationLog(**notification, status="pending", retries_attempted=0)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_notification_log(db: Session, notification_id: int):
    return db.query(models.NotificationLog).filter(models.NotificationLog.id == notification_id).first()

def update_notification_log_status(db: Session, notification_id: int, status: str, details: str = None):
    db_notification = db.query(models.NotificationLog).filter(models.NotificationLog.id == notification_id).first()
    if db_notification:
        db_notification.status = status
        if details:
            db_notification.details = details
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
    return db_notification

def increment_notification_retries(db: Session, notification_id: int):
    db_notification = db.query(models.NotificationLog).filter(models.NotificationLog.id == notification_id).first()
    if db_notification:
        db_notification.retries_attempted += 1
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
    return db_notification

def create_user_preferences(db: Session, preferences: schemas.UserPreferencesCreate):
    db_preferences = models.UserPreferences(**preferences.dict())
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def get_user_preferences(db: Session, user_id: int):
    return db.query(models.UserPreferences).filter(models.UserPreferences.user_id == user_id).first()

def update_user_preferences(db: Session, user_id: int, preferences: schemas.UserPreferencesUpdate):
    db_preferences = db.query(models.UserPreferences).filter(models.UserPreferences.user_id == user_id).first()
    if db_preferences:
        for key, value in preferences.dict(exclude_unset=True).items():
            setattr(db_preferences, key, value)
        db.add(db_preferences)
        db.commit()
        db.refresh(db_preferences)
    return db_preferences

def delete_user_preferences(db: Session, user_id: int):
    db_preferences = db.query(models.UserPreferences).filter(models.UserPreferences.user_id == user_id).first()
    if db_preferences:
        db.delete(db_preferences)
        db.commit()
    return db_preferences
