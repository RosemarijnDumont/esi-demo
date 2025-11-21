
# This file is assumed to exist and contain `get_db` for database session management.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Replace with your actual database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
