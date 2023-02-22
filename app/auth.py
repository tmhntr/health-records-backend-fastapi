
import os
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models, schemas

from app.controller import get_user_by_email
from app.dependencies import get_db
from app.utils import verify_password
from dotenv import load_dotenv
from app.env import env


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# OAuth settings
GOOGLE_CLIENT_ID = env.get('GOOGLE_CLIENT_SECRET') or None
GOOGLE_CLIENT_SECRET = env.get('GOOGLE_CLIENT_ID') or None
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

# Set up oauth
config_data = {'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
               'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET}
config = Config(environ=config_data)
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# create secret key with command: openssl rand -hex 32
SECRET_KEY = env.get("SECRET_KEY")
ALGORITHM = "HS256"



async def authenticate_user( email: str, password: str, db: Session = Depends(get_db)) -> schemas.User:
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user



def create_access_token(data: dict, expires_delta=timedelta(minutes=30)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


