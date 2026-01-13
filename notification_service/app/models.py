from sqlalchemy import Column, Integer, String, DateTime, func
from core.db import Base

class NotificationLog(Base):
    __tablename__ = "notification_logs"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String, index=True)
    message = Column(String)
    type = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
