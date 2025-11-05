from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamResponse
from app.utils.jwt_verify import verify_token

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", response_model=TeamResponse)
async def create_team(data: TeamCreate, db: AsyncSession = Depends(get_db), _: dict = Depends(verify_token)):
    team = Team(name=data.name, description=data.description)
    db.add(team)
    await db.commit()
    await db.refresh(team)
    return team

@router.get("/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db), _: dict = Depends(verify_token)):
    team = await db.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team
