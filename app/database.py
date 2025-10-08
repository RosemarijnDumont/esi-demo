from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure the database URL. For simplicity, using SQLite here.
# In a production environment, this would be an environment variable or a more robust configuration.
SQLALCHEMY_DATABASE_URL = "sqlite:///./ideas.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
