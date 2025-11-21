
# This file is assumed to exist and contain user CRUD operations.
from sqlalchemy.orm import Session

from app.models.user import User as UserModel

def get_user_by_id(db: Session, user_id: int):
    """Retrieves a user by their ID."""
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Retrieves a user by their email."""
    return db.query(UserModel).filter(UserModel.email == email).first()
