from pydantic import BaseModel
from datetime import datetime

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    task_id: int
    user_id: int

class CommentResponse(CommentBase):
    id: int
    task_id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
