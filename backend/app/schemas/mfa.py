
from pydantic import BaseModel, Field
from typing import Optional

class MFADeviceBase(BaseModel):
    device_name: str = Field(..., description="A human-readable name for the MFA device (e.g., 'My Phone Authenticator')")
    device_type: str = Field("TOTP", description="Type of MFA device (e.g., 'TOTP', 'Push')")

class MFADeviceCreate(MFADeviceBase):
    pass

class MFADeviceUpdate(MFADeviceBase):
    device_name: Optional[str] = Field(None, description="Optional: New name for the MFA device")
    is_verified: Optional[bool] = Field(None, description="Whether the MFA device has been verified")
    is_preferred: Optional[bool] = Field(None, description="Whether this is the preferred MFA device for the user")

class MFADevice(MFADeviceBase):
    id: int
    user_id: int
    secret_key: str = Field(..., description="The secret key for the MFA device (should be encrypted in production)")
    provisioning_uri: str = Field(..., description="The URI used to provision the authenticator app")
    is_verified: bool
    is_preferred: bool

    # This is a transient field for returning the QR code during enrollment
    qr_code_image: Optional[str] = Field(None, description="Base64 encoded PNG image of the QR code, for enrollment only")

    class Config:
        orm_mode = True
