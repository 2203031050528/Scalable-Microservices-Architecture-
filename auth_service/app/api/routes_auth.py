from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.core.security import verify_password, create_access_token

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
