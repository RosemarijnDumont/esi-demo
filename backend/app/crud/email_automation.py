from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.models.email_automation import AutomationRule, EmailTemplate, EmailLog
from backend.app.schemas.email_automation import (
    AutomationRuleCreate, AutomationRuleUpdate,
    EmailTemplateCreate, EmailTemplateUpdate,
    EmailLogCreate
)

def create_automation_rule(db: Session, rule: AutomationRuleCreate):
    db_rule = AutomationRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_automation_rules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AutomationRule).offset(skip).limit(limit).all()

def get_automation_rule(db: Session, rule_id: int):
    return db.query(AutomationRule).filter(AutomationRule.id == rule_id).first()

def update_automation_rule(
    db: Session, rule_id: int, rule: AutomationRuleUpdate
):
    db_rule = db.query(AutomationRule).filter(AutomationRule.id == rule_id).first()
    if db_rule:
        for key, value in rule.dict(exclude_unset=True).items():
            setattr(db_rule, key, value)
        db.commit()
        db.refresh(db_rule)
    return db_rule

def delete_automation_rule(db: Session, rule_id: int):
    db_rule = db.query(AutomationRule).filter(AutomationRule.id == rule_id).first()
    if db_rule:
        db.delete(db_rule)
        db.commit()
    return db_rule

def create_email_template(db: Session, template: EmailTemplateCreate):
    db_template = EmailTemplate(**template.dict())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template

def get_email_templates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EmailTemplate).offset(skip).limit(limit).all()

def get_email_template(db: Session, template_id: int):
    return db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()

def update_email_template(
    db: Session, template_id: int, template: EmailTemplateUpdate
):
    db_template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
    if db_template:
        for key, value in template.dict(exclude_unset=True).items():
            setattr(db_template, key, value)
        db.commit()
        db.refresh(db_template)
    return db_template

def delete_email_template(db: Session, template_id: int):
    db_template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
    if db_template:
        db.delete(db_template)
        db.commit()
    return db_template

def create_email_log(db: Session, email_log: EmailLogCreate):
    db_email_log = EmailLog(**email_log.dict())
    db.add(db_email_log)
    db.commit()
    db.refresh(db_email_log)
    return db_email_log

def get_email_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EmailLog).offset(skip).limit(limit).all()

def get_email_log(db: Session, log_id: int):
    return db.query(EmailLog).filter(EmailLog.id == log_id).first()
