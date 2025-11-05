from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = "user"

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    team_id: Optional[int]

    class Config:
        from_attributes = True
