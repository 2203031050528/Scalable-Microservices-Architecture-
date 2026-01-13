from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.models.task import Task
from app.schema.task import TaskCreate, TaskResponse
from app.utils.jwt_varify import verify_token

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
async def create_task(data: TaskCreate, db: AsyncSession = Depends(get_db), _: dict = Depends(verify_token)):
    task = Task(**data.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
