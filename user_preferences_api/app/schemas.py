
from pydantic import BaseModel
from typing import Optional

class NotificationPreferenceBase(BaseModel):
    email_enabled: Optional[bool] = True
    in_app_enabled: Optional[bool] = True
    email_promotions: Optional[bool] = True
    in_app_promotions: Optional[bool] = True
    email_security_alerts: Optional[bool] = True
    in_app_security_alerts: Optional[bool] = True
    email_system_updates: Optional[bool] = True
    in_app_system_updates: Optional[bool] = True

class NotificationPreferenceCreate(NotificationPreferenceBase):
    user_id: int

class NotificationPreferenceUpdate(NotificationPreferenceBase):
    pass

class NotificationPreference(NotificationPreferenceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

# Schema for authentication (simplified)
class User(BaseModel):
    id: int
    username: str
    email: str
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

