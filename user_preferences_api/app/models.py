
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True)
    email_enabled = Column(Boolean, default=True)
    in_app_enabled = Column(Boolean, default=True)
    email_promotions = Column(Boolean, default=True)
    in_app_promotions = Column(Boolean, default=True)
    email_security_alerts = Column(Boolean, default=True)
    in_app_security_alerts = Column(Boolean, default=True)
    email_system_updates = Column(Boolean, default=True)
    in_app_system_updates = Column(Boolean, default=True)

