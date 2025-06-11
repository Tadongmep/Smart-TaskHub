from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate


router = APIRouter()


@router.post("/signup", response_model=UserCreate)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserCreate).filter(
        UserCreate.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.hash_password(user.password)
    user = User(
        email=user.email,
        full_name=user.full_name,
        password_hash=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    """
    User signup endpoint.
    """
    # Here you would typically hash the password and save the user to the database
    # For now, we will just return the user data as is
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = security.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}