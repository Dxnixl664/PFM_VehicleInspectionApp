from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str


class TokenData(BaseModel):
    username: Optional[str] = None