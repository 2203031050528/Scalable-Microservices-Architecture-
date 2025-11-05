from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.models.project import Project
from app.schema.project import ProjectCreate, ProjectResponse
from app.utils.jwt_varify import verify_token

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ProjectResponse)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db), _: dict = Depends(verify_token)):
    project = Project(**data.dict())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@router.get("/", response_model=list[ProjectResponse])
async def list_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM projects")
    projects = result.fetchall()
    return [dict(p._mapping) for p in projects]
