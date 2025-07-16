from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(frozen=True)


class User(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(frozen=True)


class UserOutput(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    hashed_password: str

    model_config = ConfigDict(
        frozen=True,
        extra="forbid"
    )


class UserCreateInput(UserBase):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    raw_password: str

    model_config = ConfigDict(
        extra="forbid",  
        frozen=True      
    )


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    hashed_password: Optional[str] = None
