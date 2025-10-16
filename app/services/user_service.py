
from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, user_data: dict) -> User:
    if not all(k in user_data for k in ("name", "email", "role")):
        raise ValueError("Missing user data fields (name, email, role).")

    if user_data["role"] not in ["user", "admin", "guest"]:
        raise ValueError("Invalid role. Must be 'user', 'admin', or 'guest'.")

    user = User(name=user_data["name"], email=user_data["email"], role=user_data["role"])
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e
