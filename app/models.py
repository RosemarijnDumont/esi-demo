from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Idea(Base):
    __tablename__ = "ideas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(String, nullable=False)
    submitter_name = Column(String(255), nullable=False)
    submitter_email = Column(String(255), nullable=False)
    submission_timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Idea(id={self.id}, title='{self.title}', submitter_name='{self.submitter_name}')>"
