
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from pydantic import ValidationError

from data_model import DayOfWeek, AssignmentType, Base
from config_api import (
    get_db, create_team, get_team, get_team_by_hcat_id, get_all_teams, update_team, delete_team,
    create_schedule, get_schedule, get_all_schedules, update_schedule, delete_schedule,
    create_team_assignment, get_team_assignment, get_assignments_for_schedule, delete_team_assignment,
    get_audit_logs, trigger_ad_hoc_cleaning,
    TeamCreate, TeamUpdate, TeamInDB, 
    ScheduleCreate, ScheduleUpdate, ScheduleInDB,
    AssignmentCreate, AssignmentInDB,
    AdHocRequest
)

# --- FastAPI Application Setup ---

app = FastAPI(title="Kitchen Cleaning Configuration API", version="1.0.0")

@app.on_event("startup")
def on_startup():
    # This ensures tables are created when the app starts. 
    # In a real-world app, migrations would be handled separately.
    from sqlalchemy import create_engine
    from config_api import DATABASE_URL
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    print("Database tables checked/created.")

# --- Welcome Endpoint ---
@app.get("/", summary="Root", tags=["System"])
async def read_root():
    return {"message": "Welcome to the Kitchen Cleaning Configuration API"}

# --- Teams Endpoints ---

@app.post("/teams/", response_model=TeamInDB, status_code=status.HTTP_201_CREATED, summary="Create a new team", tags=["Teams"])
def create_team_endpoint(team: TeamCreate, db: Session = Depends(get_db)):
    try:
        db_team = create_team(db, team)
        if not db_team: # Should not happen if create_team is robust, but as a safeguard
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create team")
        return db_team
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/teams/", response_model=List[TeamInDB], summary="Get all teams", tags=["Teams"])
def read_teams_endpoint(db: Session = Depends(get_db)):
    return get_all_teams(db)

@app.get("/teams/{team_id}", response_model=TeamInDB, summary="Get a team by ID", tags=["Teams"])
def read_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    team = get_team(db, team_id)
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return team

@app.put("/teams/{team_id}", response_model=TeamInDB, summary="Update an existing team", tags=["Teams"])
def update_team_endpoint(team_id: int, team: TeamUpdate, db: Session = Depends(get_db)):
    db_team = update_team(db, team_id, team)
    if db_team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return db_team

@app.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a team", tags=["Teams"])
def delete_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    success = delete_team(db, team_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
    return # No content on success

# --- Schedules Endpoints ---

@app.post("/schedules/", response_model=ScheduleInDB, status_code=status.HTTP_201_CREATED, summary="Create a new cleaning schedule", tags=["Schedules"])
def create_schedule_endpoint(schedule: ScheduleCreate, db: Session = Depends(get_db)):
    try:
        db_schedule = create_schedule(db, schedule)
        if not db_schedule:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create schedule")
        return db_schedule
    except ValidationError as e: # Catch pydantic validation errors
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/schedules/", response_model=List[ScheduleInDB], summary="Get all cleaning schedules", tags=["Schedules"])
def read_schedules_endpoint(db: Session = Depends(get_db)):
    return get_all_schedules(db)

@app.get("/schedules/{schedule_id}", response_model=ScheduleInDB, summary="Get a cleaning schedule by ID", tags=["Schedules"])
def read_schedule_endpoint(schedule_id: int, db: Session = Depends(get_db)):
    schedule = get_schedule(db, schedule_id)
    if schedule is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return schedule

@app.put("/schedules/{schedule_id}", response_model=ScheduleInDB, summary="Update an existing cleaning schedule", tags=["Schedules"])
def update_schedule_endpoint(schedule_id: int, schedule: ScheduleUpdate, db: Session = Depends(get_db)):
    try:
        db_schedule = update_schedule(db, schedule_id, schedule)
        if db_schedule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        return db_schedule
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.delete("/schedules/{schedule_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a cleaning schedule", tags=["Schedules"])
def delete_schedule_endpoint(schedule_id: int, db: Session = Depends(get_db)):
    success = delete_schedule(db, schedule_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return # No content on success

# --- Team Assignments Endpoints ---

@app.post("/assignments/", response_model=AssignmentInDB, status_code=status.HTTP_201_CREATED, summary="Assign a team to a schedule", tags=["Assignments"])
def create_assignment_endpoint(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    try:
        # Basic validation that schedule and team exist
        if not get_schedule(db, assignment.schedule_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        if not get_team(db, assignment.team_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

        db_assignment = create_team_assignment(db, assignment)
        if not db_assignment:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create assignment")
        return db_assignment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.get("/assignments/{assignment_id}", response_model=AssignmentInDB, summary="Get a team assignment by ID", tags=["Assignments"])
def read_assignment_endpoint(assignment_id: int, db: Session = Depends(get_db)):
    assignment = get_team_assignment(db, assignment_id)
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return assignment

@app.get("/schedules/{schedule_id}/assignments/", response_model=List[AssignmentInDB], summary="Get all assignments for a schedule", tags=["Assignments"])
def read_assignments_for_schedule_endpoint(schedule_id: int, db: Session = Depends(get_db)):
    if not get_schedule(db, schedule_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
    return get_assignments_for_schedule(db, schedule_id)

@app.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a team assignment", tags=["Assignments"])
def delete_assignment_endpoint(assignment_id: int, db: Session = Depends(get_db)):
    success = delete_team_assignment(db, assignment_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    return # No content on success

# --- Audit Logs Endpoint ---

@app.get("/audit_logs/", summary="Get configuration audit logs", tags=["Audit"])
def get_audit_logs_endpoint(entity_type: Optional[str] = None, entity_id: Optional[int] = None, db: Session = Depends(get_db)):
    return get_audit_logs(db, entity_type, entity_id)

# --- Ad-hoc Cleaning Endpoint ---

@app.post("/ad_hoc_cleaning/", summary="Trigger an ad-hoc cleaning request", tags=["Ad-Hoc"])
def trigger_ad_hoc_cleaning_endpoint(request: AdHocRequest, db: Session = Depends(get_db)):
    try:
        # The actual HCAT sending logic would be here or in a separate service.
        # For this exercise, the `trigger_ad_hoc_cleaning` function in config_api.py
        # simulates the HCAT trigger and logs the delivery confirmation.
        result = trigger_ad_hoc_cleaning(db, request, user="api_trigger") # User can be dynamic later
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
