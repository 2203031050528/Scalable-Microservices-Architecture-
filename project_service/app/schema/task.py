from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str]
    status: Optional[str] = "To-do"
    priority: Optional[str] = "Medium"
    due_date: Optional[datetime]
    assigned_to: Optional[int]

class TaskCreate(TaskBase):
    project_id: int

class TaskResponse(TaskBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True
