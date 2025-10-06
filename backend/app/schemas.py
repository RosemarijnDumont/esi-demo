
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    is_active: bool
    avatar_url: Optional[str] = None # Added avatar_url field

    class Config:
        orm_mode = True

# Schema for updating user avatar (optional, could use UserInDB directly)
class User(UserInDB):
    pass
