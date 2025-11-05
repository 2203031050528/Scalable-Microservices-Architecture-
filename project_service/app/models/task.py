from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(255))
    status = Column(String(20), default="To-do")  # To-do, In Progress, Completed
    priority = Column(String(10), default="Medium")  # Low, Medium, High
    due_date = Column(DateTime)
    project_id = Column(Integer, ForeignKey("projects.id"))
    assigned_to = Column(Integer)  # user_id

    project = relationship("Project", back_populates="tasks")
