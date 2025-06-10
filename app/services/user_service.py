from sqlalchemy.orm import Session
from app.models.user import User # Assuming your User model is in app/models/user.py
from app.schemas.user import UserCreate
from passlib.context import CryptContext
import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    current_timestamp = int(time.time()) # Unix timestamp
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