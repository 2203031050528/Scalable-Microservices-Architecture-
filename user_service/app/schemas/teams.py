from pydantic import BaseModel
from typing import Optional, List
from app.schemas.user import UserResponse

class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int
    members: List[UserResponse] = []

    class Config:
        from_attributes = True
