from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.utils.jwt_varify import verify_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute("SELECT * FROM users")
    users = result.fetchall()
    return [dict(u._mapping) for u in users]

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserCreate, db: AsyncSession = Depends(get_db), _: dict = Depends(verify_token)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = data.name
    user.role = data.role
    await db.commit()
    await db.refresh(user)
    return user
