from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_db, Base, engine
from .schema import NotificationCreate
from .crud import create_notification
from .services.email_service import send_email
from .redis_client import get_redis
import asyncio

app = FastAPI(title="Notification Service")

@app.on_event("startup")
async def startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/notifications/")
async def send_notification(notification: NotificationCreate, db: AsyncSession = Depends(get_db)):
    # Save to DB
    notif = await create_notification(db, notification)
    
    # Push to Redis queue
    redis = await get_redis()
    await redis.lpush("notifications_queue", f"{notif.id}")
    
    # Send email asynchronously
    asyncio.create_task(send_email(notification.recipient, f"New {notification.type}", notification.message))
    
    return {"msg": "Notification queued and email sent", "id": notif.id}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
