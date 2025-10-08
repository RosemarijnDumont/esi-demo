
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configure your database connection string here
# For example, using SQLite for simplicity in development:
SQLALCHEMY_DATABASE_URL = "sqlite:///./notifications.db"
# For PostgreSQL:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@host:port/dbname"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
