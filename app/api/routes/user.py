from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user
from app.crud.user import update_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from sqlalchemy.orm import Session
from app.core.db import get_db

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/update", response_model=UserResponse)
async def update_user_profile(user_update: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user_update.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_updated_user = update_user(db, user_update, current_user)
    return db_updated_user
