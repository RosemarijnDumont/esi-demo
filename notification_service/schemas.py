
from pydantic import BaseModel, EmailStr
from typing import Dict, Any, Optional
import datetime

class NotificationCreate(BaseModel):
    recipient: str  # e.g., user ID, email address
    notification_type: str  # e.g., 'email', 'in-app'
    template_name: str
    template_data: Dict[str, Any] = {}

class NotificationResponse(BaseModel):
    message: str
    notification_id: Optional[int] = None

class NotificationLog(BaseModel):
    id: int
    recipient: str
    notification_type: str
    template_name: str
    template_data: Dict[str, Any]
    status: str
    details: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    retries_attempted: int

    class Config:
        orm_mode = True

class UserPreferencesBase(BaseModel):
    user_id: int
    email_enabled: bool = True
    in_app_enabled: bool = True
    marketing_emails_enabled: bool = False

class UserPreferencesCreate(UserPreferencesBase):
    pass

class UserPreferencesUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    in_app_enabled: Optional[bool] = None
    marketing_emails_enabled: Optional[bool] = None

class UserPreferences(UserPreferencesBase):
    id: int

    class Config:
        orm_mode = True

class NotificationProcessRequest(BaseModel):
    notification_id: int
    status: str
    details: Optional[str] = None
    retries_attempted: int = 0
