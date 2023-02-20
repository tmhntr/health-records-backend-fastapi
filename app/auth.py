
import os
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from datetime import datetime, timedelta
from jose import jwt
from sqlalchemy.orm import Session

from app.controller import get_user_by_email
from app.utils import verify_password


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


SECRET_KEY = "f8cf8fc4b3f31a1e1e0de2b84286130dc04715430cdb9020ca0986cda7071d8f"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta=timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
