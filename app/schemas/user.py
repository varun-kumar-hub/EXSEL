from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    role: str = "viewer"
    is_active: bool = True


class UserCreate(BaseModel):
    email: str
    password: str = Field(..., min_length=8)
    confirm_password: str
    full_name: str
    terms_accepted: bool = True


class UserLogin(BaseModel):
    email: str
    password: str
    remember_me: bool = False


class UserResponse(UserBase):
    id: str
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)
    confirm_password: str
