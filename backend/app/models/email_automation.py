from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from backend.app.db.base_class import Base

class AutomationRule(Base):
    __tablename__ = "automation_rules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    trigger_event = Column(String, nullable=False) # e.g., "ticket_status_change"
    condition_json = Column(Text) # JSON string for complex conditions
    template_id = Column(Integer, ForeignKey("email_templates.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    template = relationship("EmailTemplate", back_populates="rules")

class EmailTemplate(Base):
    __tablename__ = "email_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False) # jinja2 template string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    rules = relationship("AutomationRule", back_populates="template")
    email_logs = relationship("EmailLog", back_populates="template")

class EmailLog(Base):
    __tablename__ = "email_logs"
    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    body_sent = Column(Text, nullable=False)
    template_id = Column(Integer, ForeignKey("email_templates.id"), nullable=True)
    automation_rule_id = Column(Integer, ForeignKey("automation_rules.id"), nullable=True)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="SENT") # e.g., SENT, FAILED, PENDING
    error_message = Column(Text, nullable=True)

    template = relationship("EmailTemplate", back_populates="email_logs")
    rule = relationship("AutomationRule")

