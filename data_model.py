
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import enum

Base = declarative_base()

class DayOfWeek(enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"

class AssignmentType(enum.Enum):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    BI_WEEKLY = "Bi-Weekly"
    MONTHLY = "Monthly"
    AD_HOC = "Ad-Hoc"

class KitchenCleaningSchedule(Base):
    __tablename__ = 'kitchen_cleaning_schedules'

    id = Column(Integer, primary_key=True)
    schedule_name = Column(String, nullable=False, unique=True)
    assignment_type = Column(Enum(AssignmentType), nullable=False)
    day_of_week = Column(Enum(DayOfWeek), nullable=True)  # For weekly/bi-weekly schedules
    day_of_month = Column(Integer, nullable=True)         # For monthly schedules
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)

    assignments = relationship("TeamAssignment", back_populates="schedule")

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    team_name = Column(String, nullable=False, unique=True)
    team_hcat_id = Column(String, nullable=False, unique=True) # ID used for HCAT system

    assignments = relationship("TeamAssignment", back_populates="team")

class TeamAssignment(Base):
    __tablename__ = 'team_assignments'

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('kitchen_cleaning_schedules.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=False)

    schedule = relationship("KitchenCleaningSchedule", back_populates="assignments")
    team = relationship("Team", back_populates="assignments")

    __table_args__ = (UniqueConstraint('schedule_id', 'team_id', name='_schedule_team_uc'),)

class ConfigurationAudit(Base):
    __tablename__ = 'configuration_audits'

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=func.now())
    user = Column(String, nullable=False)
    action = Column(String, nullable=False)
    entity_type = Column(String, nullable=False)
    entity_id = Column(Integer, nullable=False)
    old_value = Column(JSON, nullable=True) # Store old state as JSON
    new_value = Column(JSON, nullable=True) # Store new state as JSON

from sqlalchemy import UniqueConstraint, DateTime, func
from sqlalchemy.dialects.postgresql import JSON # Using PostgreSQL's JSON type for audit table

# Example of how to set up the database (for SQLite in this example)
# DATABASE_URL = "sqlite:///./kitchen_cleaning.db"
# engine = create_engine(DATABASE_URL)
# Base.metadata.create_all(engine)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
