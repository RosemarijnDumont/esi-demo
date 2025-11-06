from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class AutomationRuleBase(BaseModel):
    name: str
    trigger_event: str
    condition_json: Optional[str] = None # JSON string for conditions
    template_id: Optional[int] = None
    is_active: Optional[bool] = True

class AutomationRuleCreate(AutomationRuleBase):
    pass

class AutomationRuleUpdate(AutomationRuleBase):
    name: Optional[str] = None
    trigger_event: Optional[str] = None

class AutomationRule(AutomationRuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class EmailTemplateBase(BaseModel):
    name: str
    subject: str
    body: str

class EmailTemplateCreate(EmailTemplateBase):
    pass

class EmailTemplateUpdate(EmailTemplateBase):
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None

class EmailTemplate(EmailTemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class EmailLogBase(BaseModel):
    recipient_email: EmailStr
    subject: str
    body_sent: str
    template_id: Optional[int] = None
    automation_rule_id: Optional[int] = None
    status: Optional[str] = "SENT"
    error_message: Optional[str] = None

class EmailLogCreate(EmailLogBase):
    pass

class EmailLog(EmailLogBase):
    id: int
    sent_at: datetime

    class Config:
        orm_mode = True
