from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from app.crud.user import create_user
from app.utils import security
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.core.config import settings

router = APIRouter()


@router.post("/signup", response_model=UserResponse)
# @router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = create_user(db, user)
    """
    User signup endpoint.
    """
    # Here you would typically hash the password and save the user to the database
    # For now, we will just return the user data as is
    return db_user


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=401, detail="Incorrect email or password")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    refresh_token = security.create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str = Body(...)):
    try:
        payload = security.decode_token(
            refresh_token, settings.REFRESH_SECRET_KEY)
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")

    access_token = security.create_access_token(data={"sub": user_id})
    new_refresh_token = security.create_refresh_token(data={"sub": user_id})
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
