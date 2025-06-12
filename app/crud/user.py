from fastapi import Depends
from sqlalchemy.orm import Session
from api.deps import get_current_user
from utils.security import get_password_hash
from models.user import User  # Assuming your User model is in app/models/user.py
from schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext
import time


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    current_timestamp = int(time.time())  # Unix timestamp
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        full_name=user.full_name,
        created_at=current_timestamp,
        updated_at=current_timestamp
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_update: UserUpdate, current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        return None

    if user_update.email:
        user.email = user_update.email
    if user_update.full_name:
        user.full_name = user_update.full_name
    if user_update.avatar_url:
        user.avatar_url = user_update.avatar_url

    current_timestamp = int(time.time())
    user.updated_at = current_timestamp

    db.commit()
    db.refresh(user)
    return user
