
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.models.mfa import MFADevice as MFADeviceModel
from app.schemas.mfa import MFADeviceCreate, MFADeviceUpdate

def create_mfa_device(db: Session, mfa_device: Dict[str, Any]):
    """Creates a new MFA device record in the database."""
    db_mfa_device = MFADeviceModel(**mfa_device)
    db.add(db_mfa_device)
    db.commit()
    db.refresh(db_mfa_device)
    return db_mfa_device

def get_mfa_device_by_id(db: Session, mfa_device_id: int):
    """Retrieves an MFA device by its ID."""
    return db.query(MFADeviceModel).filter(MFADeviceModel.id == mfa_device_id).first()

def get_mfa_devices_by_user(db: Session, user_id: int) -> List[MFADeviceModel]:
    """Retrieves all MFA devices for a given user."""
    return db.query(MFADeviceModel).filter(MFADeviceModel.user_id == user_id).all()

def get_preferred_mfa_device_by_user(db: Session, user_id: int) -> MFADeviceModel | None:
    """Retrieves the preferred MFA device for a given user."""
    return (db.query(MFADeviceModel)
            .filter(MFADeviceModel.user_id == user_id, MFADeviceModel.is_preferred == True)
            .first())

def update_mfa_device(
    db: Session, mfa_device_id: int, mfa_device_in: MFADeviceUpdate
):
    """Updates an existing MFA device record."""
    db_mfa_device = get_mfa_device_by_id(db, mfa_device_id)
    if not db_mfa_device:
        return None
    update_data = mfa_device_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_mfa_device, field, value)
    db.add(db_mfa_device)
    db.commit()
    db.refresh(db_mfa_device)
    return db_mfa_device

def delete_mfa_device(db: Session, mfa_device_id: int):
    """Deletes an MFA device record from the database."""
    db_mfa_device = get_mfa_device_by_id(db, mfa_device_id)
    if db_mfa_device:
        db.delete(db_mfa_device)
        db.commit()
    return db_mfa_device
