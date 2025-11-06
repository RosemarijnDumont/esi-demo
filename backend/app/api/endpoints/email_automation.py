from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.app.schemas.email_automation import (
    AutomationRuleCreate, AutomationRule, AutomationRuleUpdate,
    EmailTemplateCreate, EmailTemplate, EmailTemplateUpdate,
    EmailLogCreate, EmailLog
)
from backend.app.crud import email_automation as crud
from backend.app.db.session import get_db

router = APIRouter()

# --- Automation Rule Endpoints ---

@router.post("/rules/", response_model=AutomationRule)
def create_automation_rule(
    rule: AutomationRuleCreate, db: Session = Depends(get_db)
):
    return crud.create_automation_rule(db=db, rule=rule)

@router.get("/rules/", response_model=List[AutomationRule])
def read_automation_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_automation_rules(db=db, skip=skip, limit=limit)

@router.get("/rules/{rule_id}/", response_model=AutomationRule)
def read_automation_rule(rule_id: int, db: Session = Depends(get_db)):
    db_rule = crud.get_automation_rule(db=db, rule_id=rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="AutomationRule not found")
    return db_rule

@router.put("/rules/{rule_id}/", response_model=AutomationRule)
def update_automation_rule(
    rule_id: int, rule: AutomationRuleUpdate, db: Session = Depends(get_db)
):
    db_rule = crud.update_automation_rule(db=db, rule_id=rule_id, rule=rule)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="AutomationRule not found")
    return db_rule

@router.delete("/rules/{rule_id}/", response_model=AutomationRule)
def delete_automation_rule(rule_id: int, db: Session = Depends(get_db)):
    db_rule = crud.delete_automation_rule(db=db, rule_id=rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="AutomationRule not found")
    return db_rule

# --- Email Template Endpoints ---

@router.post("/templates/", response_model=EmailTemplate)
def create_email_template(
    template: EmailTemplateCreate, db: Session = Depends(get_db)
):
    return crud.create_email_template(db=db, template=template)

@router.get("/templates/", response_model=List[EmailTemplate])
def read_email_templates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_email_templates(db=db, skip=skip, limit=limit)

@router.get("/templates/{template_id}/", response_model=EmailTemplate)
def read_email_template(template_id: int, db: Session = Depends(get_db)):
    db_template = crud.get_email_template(db=db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="EmailTemplate not found")
    return db_template

@router.put("/templates/{template_id}/", response_model=EmailTemplate)
def update_email_template(
    template_id: int, template: EmailTemplateUpdate, db: Session = Depends(get_db)
):
    db_template = crud.update_email_template(db=db, template_id=template_id, template=template)
    if db_template is None:
        raise HTTPException(status_code=404, detail="EmailTemplate not found")
    return db_template

@router.delete("/templates/{template_id}/", response_model=EmailTemplate)
def delete_email_template(template_id: int, db: Session = Depends(get_db)):
    db_template = crud.delete_email_template(db=db, template_id=template_id)
    if db_template is None:
        raise HTTPException(status_code=404, detail="EmailTemplate not found")
    return db_template

# --- Email Log Endpoints ---

# This endpoint is primarily for viewing logs, creation happens internally in email_service
@router.get("/email-logs/", response_model=List[EmailLog])
def read_email_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_email_logs(db=db, skip=skip, limit=limit)

@router.get("/email-logs/{log_id}/", response_model=EmailLog)
def read_email_log(log_id: int, db: Session = Depends(get_db)):
    db_log = crud.get_email_log(db=db, log_id=log_id)
    if db_log is None:
        raise HTTPException(status_code=404, detail="EmailLog not found")
    return db_log
