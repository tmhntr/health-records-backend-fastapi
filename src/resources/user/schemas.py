from typing import Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    key: str
    user_id: str


class User(UserBase):
    is_active: bool
    id: str
    # records: list[Record] = []

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None
