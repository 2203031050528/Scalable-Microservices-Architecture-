from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.core.security import verify_password, create_access_token
from app.core.deps import get_current_user
from app.core.redis_client import get_redis
from app.db.models import *
from app.utils.email_utils import send_email
from app.core.security import *
from app.core.deps import *
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup")
def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="Email already exists")
    user = crud.create_user(db, username, email, password)
    return {"message": "User registered", "user_id": user.id}

@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model= UserOut)
def get_me(current_user=Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    redis = await get_redis()
    await redis.setex(f"blacklist:{token}", 3600, "true")  # token expires after 1h
    await redis.close()
    return {"msg": "Logged out successfully"}

@router.post("/reset-password")
async def reset_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")    
    
    token = create_access_token({"sub": user.email})
    reset_link = f"http://localhost:8000/auth/reset-password/confirm?token={token}"
    
    subject = "Reset Your Password"
    body = f"""
    <h3>Password Reset Request</h3>
    <p>Click below to reset your password:</p>
    <a href="{reset_link}" style="padding:10px 20px;background:#007bff;color:white;border-radius:5px;text-decoration:none;">
        Reset Password
    </a>
    """
    
    await send_email(user.email, subject, body)  # ✅ correct usage
    
    return {"msg": f"Password reset email sent to {user.email}"}


@router.post("/reset-password/confirm")
def confirm_reset(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        email = payload.get("sub")
        user = db.query(User).filter(User.email == email).first()
        user.hashed_password = hash_password(new_password)
        db.commit()
        return {"msg": "Password updated successfully"}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
