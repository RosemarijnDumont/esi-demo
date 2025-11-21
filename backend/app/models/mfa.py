
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class MFADevice(Base):
    """SQLAlchemy model for storing MFA device information."""
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    device_name = Column(String, index=True, nullable=False)
    device_type = Column(String, default="TOTP") # e.g., TOTP, Push
    secret_key = Column(String, nullable=False) # Store encrypted in production
    provisioning_uri = Column(String, nullable=False)
    is_verified = Column(Boolean, default=False)
    is_preferred = Column(Boolean, default=False)

    user = relationship("User", back_populates="mfa_devices")
