from pydantic import BaseModel
from typing import Optional, List
from app.schema.task import TaskResponse

class ProjectBase(BaseModel):
    name: str
    description: Optional[str]

class ProjectCreate(ProjectBase):
    owner_id: int

class ProjectResponse(ProjectBase):
    id: int
    tasks: List[TaskResponse] = []

    class Config:
        orm_mode = True
