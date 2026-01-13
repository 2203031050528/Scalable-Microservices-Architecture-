from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def create_notification(db: AsyncSession, notification: schemas.NotificationCreate):
    new_notification = models.NotificationLog(
        recipient=notification.recipient,
        message=notification.message,
        type=notification.type
    )
    db.add(new_notification)
    await db.commit()
    await db.refresh(new_notification)
    return new_notification
