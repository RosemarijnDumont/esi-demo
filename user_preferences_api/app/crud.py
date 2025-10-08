
from sqlalchemy.orm import Session

from . import models, schemas

def get_user_preferences(db: Session, user_id: int):
    return db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id).first()

def create_user_preferences(db: Session, user_id: int, preferences: schemas.NotificationPreferenceCreate):
    db_preferences = models.UserPreference(**preferences.dict(), user_id=user_id)
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    return db_preferences

def update_user_preferences(db: Session, user_id: int, preferences: schemas.NotificationPreferenceUpdate):
    db_preferences = db.query(models.UserPreference).filter(models.UserPreference.user_id == user_id).first()
    if db_preferences:
        for key, value in preferences.dict(exclude_unset=True).items():
            setattr(db_preferences, key, value)
        db.commit()
        db.refresh(db_preferences)
    return db_preferences

