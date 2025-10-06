
from typing import List, Optional
from datetime import date
from pydantic import BaseModel, Field, ValidationError, validator
from sqlalchemy.orm import Session
from data_model import KitchenCleaningSchedule, Team, TeamAssignment, ConfigurationAudit, DayOfWeek, AssignmentType, Base # Assuming these are in data_model.py
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
import json

# --- Database Setup (for demonstration, use your actual DB config) ---
DATABASE_URL = "sqlite:///./kitchen_cleaning.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine) # Create tables if they don't exist
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Pydantic Models for API Request/Response Validation ---

class TeamBase(BaseModel):
    team_name: str = Field(..., min_length=1)
    team_hcat_id: str = Field(..., min_length=1)

class TeamCreate(TeamBase):
    pass

class TeamUpdate(TeamBase):
    team_name: Optional[str] = None
    team_hcat_id: Optional[str] = None

class TeamInDB(TeamBase):
    id: int

    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    schedule_name: str = Field(..., min_length=1)
    assignment_type: AssignmentType
    day_of_week: Optional[DayOfWeek] = None
    day_of_month: Optional[int] = Field(None, ge=1, le=31)
    start_date: date
    end_date: Optional[date] = None
    is_active: bool = True

    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values, **kwargs):
        if v and values.get('start_date') and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v
    
    @validator('day_of_week')
    def day_of_week_required_for_weekly_biweekly(cls, v, values, **kwargs):
        if values.get('assignment_type') in [AssignmentType.WEEKLY, AssignmentType.BI_WEEKLY] and v is None:
            raise ValueError('day_of_week is required for WEEKLY and BI_WEEKLY schedules')
        return v
    
    @validator('day_of_month')
    def day_of_month_required_for_monthly(cls, v, values, **kwargs):
        if values.get('assignment_type') == AssignmentType.MONTHLY and v is None:
            raise ValueError('day_of_month is required for MONTHLY schedules')
        return v

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleUpdate(ScheduleBase):
    schedule_name: Optional[str] = None
    assignment_type: Optional[AssignmentType] = None
    start_date: Optional[date] = None

class ScheduleInDB(ScheduleBase):
    id: int
    assignments: List['AssignmentInDB'] = []

    class Config:
        orm_mode = True

class AssignmentBase(BaseModel):
    schedule_id: int
    team_id: int

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentInDB(AssignmentBase):
    id: int
    schedule: Optional[ScheduleInDB] = None
    team: Optional[TeamInDB] = None

    class Config:
        orm_mode = True

class AdHocRequest(BaseModel):
    team_hcat_id: str
    notes: Optional[str] = None

# Update forward refs
ScheduleInDB.update_forward_refs()
AssignmentInDB.update_forward_refs()

# --- CRUD Operations and Configuration API ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _audit_log(db: Session, user: str, action: str, entity_type: str, entity_id: int, old_value: dict = None, new_value: dict = None):
    audit_entry = ConfigurationAudit(
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        old_value=old_value,
        new_value=new_value
    )
    db.add(audit_entry)
    db.commit()
    db.refresh(audit_entry)

# Team API
def create_team(db: Session, team: TeamCreate, user: str = "system") -> Optional[TeamInDB]:
    db_team = Team(team_name=team.team_name, team_hcat_id=team.team_hcat_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    _audit_log(db, user, "CREATE", "Team", db_team.id, new_value=team.dict())
    return TeamInDB.from_orm(db_team)

def get_team(db: Session, team_id: int) -> Optional[TeamInDB]:
    team = db.query(Team).filter(Team.id == team_id).first()
    return TeamInDB.from_orm(team) if team else None

def get_team_by_hcat_id(db: Session, team_hcat_id: str) -> Optional[TeamInDB]:
    team = db.query(Team).filter(Team.team_hcat_id == team_hcat_id).first()
    return TeamInDB.from_orm(team) if team else None

def get_all_teams(db: Session) -> List[TeamInDB]:
    teams = db.query(Team).all()
    return [TeamInDB.from_orm(team) for team in teams]

def update_team(db: Session, team_id: int, team: TeamUpdate, user: str = "system") -> Optional[TeamInDB]:
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team:
        old_values = TeamInDB.from_orm(db_team).dict()
        for key, value in team.dict(exclude_unset=True).items():
            setattr(db_team, key, value)
        db.commit()
        db.refresh(db_team)
        _audit_log(db, user, "UPDATE", "Team", db_team.id, old_value=old_values, new_value=TeamInDB.from_orm(db_team).dict())
        return TeamInDB.from_orm(db_team)
    return None

def delete_team(db: Session, team_id: int, user: str = "system") -> bool:
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team:
        db.delete(db_team)
        db.commit()
        _audit_log(db, user, "DELETE", "Team", team_id, old_value=TeamInDB.from_orm(db_team).dict())
        return True
    return False

# Schedule API
def create_schedule(db: Session, schedule: ScheduleCreate, user: str = "system") -> Optional[ScheduleInDB]:
    db_schedule = KitchenCleaningSchedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    _audit_log(db, user, "CREATE", "KitchenCleaningSchedule", db_schedule.id, new_value=schedule.dict())
    return ScheduleInDB.from_orm(db_schedule)

def get_schedule(db: Session, schedule_id: int) -> Optional[ScheduleInDB]:
    schedule = db.query(KitchenCleaningSchedule).filter(KitchenCleaningSchedule.id == schedule_id).first()
    return ScheduleInDB.from_orm(schedule) if schedule else None

def get_all_schedules(db: Session) -> List[ScheduleInDB]:
    schedules = db.query(KitchenCleaningSchedule).all()
    return [ScheduleInDB.from_orm(schedule) for schedule in schedules]

def update_schedule(db: Session, schedule_id: int, schedule: ScheduleUpdate, user: str = "system") -> Optional[ScheduleInDB]:
    db_schedule = db.query(KitchenCleaningSchedule).filter(KitchenCleaningSchedule.id == schedule_id).first()
    if db_schedule:
        old_values = ScheduleInDB.from_orm(db_schedule).dict()
        for key, value in schedule.dict(exclude_unset=True).items():
            setattr(db_schedule, key, value)
        db.commit()
        db.refresh(db_schedule)
        _audit_log(db, user, "UPDATE", "KitchenCleaningSchedule", db_schedule.id, old_value=old_values, new_value=ScheduleInDB.from_orm(db_schedule).dict())
        return ScheduleInDB.from_orm(db_schedule)
    return None

def delete_schedule(db: Session, schedule_id: int, user: str = "system") -> bool:
    db_schedule = db.query(KitchenCleaningSchedule).filter(KitchenCleaningSchedule.id == schedule_id).first()
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
        _audit_log(db, user, "DELETE", "KitchenCleaningSchedule", schedule_id, old_value=ScheduleInDB.from_orm(db_schedule).dict())
        return True
    return False

# Team Assignment API
def create_team_assignment(db: Session, assignment: AssignmentCreate, user: str = "system") -> Optional[AssignmentInDB]:
    db_assignment = TeamAssignment(schedule_id=assignment.schedule_id, team_id=assignment.team_id)
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    _audit_log(db, user, "CREATE", "TeamAssignment", db_assignment.id, new_value=assignment.dict())
    return AssignmentInDB.from_orm(db_assignment)

def get_team_assignment(db: Session, assignment_id: int) -> Optional[AssignmentInDB]:
    assignment = db.query(TeamAssignment).filter(TeamAssignment.id == assignment_id).first()
    return AssignmentInDB.from_orm(assignment) if assignment else None

def get_assignments_for_schedule(db: Session, schedule_id: int) -> List[AssignmentInDB]:
    assignments = db.query(TeamAssignment).filter(TeamAssignment.schedule_id == schedule_id).all()
    return [AssignmentInDB.from_orm(assignment) for assignment in assignments]

def delete_team_assignment(db: Session, assignment_id: int, user: str = "system") -> bool:
    db_assignment = db.query(TeamAssignment).filter(TeamAssignment.id == assignment_id).first()
    if db_assignment:
        db.delete(db_assignment)
        db.commit()
        _audit_log(db, user, "DELETE", "TeamAssignment", assignment_id, old_value=AssignmentInDB.from_orm(db_assignment).dict())
        return True
    return False

# Configuration Audit API
def get_audit_logs(db: Session, entity_type: Optional[str] = None, entity_id: Optional[int] = None) -> List[dict]:
    query = db.query(ConfigurationAudit)
    if entity_type:
        query = query.filter(ConfigurationAudit.entity_type == entity_type)
    if entity_id:
        query = query.filter(ConfigurationAudit.entity_id == entity_id)
    
    audits = query.order_by(ConfigurationAudit.timestamp.desc()).all()
    return [{
        "id": audit.id,
        "timestamp": audit.timestamp.isoformat(),
        "user": audit.user,
        "action": audit.action,
        "entity_type": audit.entity_type,
        "entity_id": audit.entity_id,
        "old_value": audit.old_value,
        "new_value": audit.new_value
    } for audit in audits]

# Ad-hoc cleaning request (example - this would likely interact with another service)
def trigger_ad_hoc_cleaning(db: Session, request: AdHocRequest, user: str = "manual") -> dict:
    team = get_team_by_hcat_id(db, request.team_hcat_id)
    if not team:
        raise ValueError(f"Team with HCAT ID {request.team_hcat_id} not found.")
    
    # In a real scenario, this would trigger an HCAT to the team. 
    # For this exercise, we'll just log it as an audit event and simulate success.
    log_message = f"Ad-hoc cleaning request triggered for team {team.team_name} (HCAT ID: {request.team_hcat_id}). Notes: {request.notes or 'No notes'}"
    _audit_log(db, user, "AD_HOC_TRIGGER", "AdHocCleaning", team.id, new_value=request.dict())
    
    # Simulate HCAT delivery confirmation
    print(f"HCAT sent to {team.team_hcat_id} for ad-hoc cleaning. Confirmation logged.")
    _audit_log(db, "system", "HCAT_DELIVERY_CONFIRMATION", "AdHocCleaning", team.id, new_value={"hcat_id": team.team_hcat_id, "status": "Delivered"})

    return {"status": "success", "message": log_message, "team_id": team.id}
