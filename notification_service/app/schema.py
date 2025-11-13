from pydantic import BaseModel, EmailStr

class NotificationCreate(BaseModel):
    recipient: EmailStr
    message: str
    type: str  # "welcome", "task_alert", etc.
