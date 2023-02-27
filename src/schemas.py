from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel


class RecordBase(BaseModel):
    description: str
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

class RecordUpdate(BaseModel):
    description: Optional[str] = None
    record_type: Optional[str] = None
    date: Optional[str] = None

    start_date: Optional[Union[str, None]] = None
    end_date: Optional[Union[str, None]] = None

    referral_to: Optional[Union[str, None]] = None

    instructions: Optional[Union[str, None]] = None
    dose: Optional[Union[str, None]] = None
    dose_unit: Optional[Union[str, None]] = None

    value: Optional[Union[str, None]] = None
    value_unit: Optional[Union[str, None]] = None


class UserBase(BaseModel):
    email: str
    oauth_id: str


class UserCreate(UserBase):
    key: str


class User(UserBase):
    id: int
    is_active: bool
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

    
class Count(BaseModel):
    count: int