from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: int
    updated_at: int

    model_config = {
        "from_attributes": True  # tells Pydantic to treat dict as an object with
    }


class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str

    model_config = {
        "from_attributes": True
    }


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None

    model_config = {
        "from_attributes": True
    }


class UserDelete(BaseModel):
    id: int

    model_config = {
        "from_attributes": True
    }


class UserListResponse(BaseModel):
    total: int
    page: int
    size: int
    items: list[UserResponse]

    model_config = {
        "from_attributes": True
    }
