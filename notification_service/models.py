
from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, index=True, nullable=False)
    notification_type = Column(String, nullable=False) # e.g., 'email', 'in-app'
    template_name = Column(String, nullable=False)
    template_data = Column(JSON, nullable=False)
    status = Column(String, default="pending", nullable=False) # e.g., 'pending', 'sent', 'failed', 'retrying'
    details = Column(String, nullable=True) # More detailed error messages or success info
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    retries_attempted = Column(Integer, default=0, nullable=False)

class UserPreferences(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    email_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)
    marketing_emails_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
