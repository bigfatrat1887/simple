from pydantic import BaseModel, UUID4
from typing import Optional


class UserCreate(BaseModel):
    email: str
    password1: str
    code: Optional[int] = None


class User(UserCreate):
    id: UUID4


class UserCheck(UserCreate):
    password2: str

