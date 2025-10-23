
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EmailTemplate(Base):
    __tablename__ = 'email_templates'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    subject = Column(String(255), nullable=False)
    body_html = Column(Text)
    body_text = Column(Text, nullable=False)
    inquiry_type_id = Column(Integer, ForeignKey('inquiry_types.id'))
    inquiry_type = relationship("InquiryType", back_populates="email_templates")

    def __repr__(self):
        return f"<EmailTemplate(id={self.id}, name='{self.name}', subject='{self.subject}')>"

class InquiryType(Base):
    __tablename__ = 'inquiry_types'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    keywords = Column(Text)  # Comma-separated keywords
    email_templates = relationship("EmailTemplate", back_populates="inquiry_type")

    def __repr__(self):
        return f"<InquiryType(id={self.id}, name='{self.name}')>"

class AutomationRule(Base):
    __tablename__ = 'automation_rules'
    id = Column(Integer, primary_key=True)
    trigger_condition = Column(String(255), nullable=False)  # e.g., 'keyword_match:billing', 'inquiry_type:refund'
    action = Column(String(255), nullable=False)  # e.g., 'send_email_template:1'

    def __repr__(self):
        return f"<AutomationRule(id={self.id}, trigger='{self.trigger_condition}', action='{self.action}')>"

