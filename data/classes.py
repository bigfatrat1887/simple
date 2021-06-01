from pydantic import BaseModel, UUID4
from typing import Optional
from random import randint


class UserBase(BaseModel):
    email: str
    password1: str
    code: Optional[int] = randint(100000, 999999)


class User(UserBase):
    id: UUID4


class UserRegister(UserBase):
    password2: str

