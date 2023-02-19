from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class RecordBase(BaseModel):
    description: Union[str, None] = None
    record_type: str
    date: str = datetime.now().strftime("%Y-%m-%d")

    start_date: Union[str, None] = None
    end_date: Union[str, None] = None

    referral_to: Union[str, None] = None

    instructions: Union[str, None] = None
    dose: Union[str, None] = None
    dose_unit: Union[str, None] = None

    value: Union[str, None] = None
    value_unit: Union[str, None] = None




class RecordCreate(RecordBase):
    pass


class Record(RecordBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    records: list[Record] = []

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

    