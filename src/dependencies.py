from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordBearer

# local imports
from src.database import SessionLocal
import logging
from src.resources.user.controller import UserController

logger = logging.getLogger(__name__)

# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="https://dev-mx-lf095.us.auth0.com/oauth/token")

async def get_current_user(user_data: schemas.TokenData = Depends(authenticate_user), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Session"},
    )
    controller = UserController(db)
    user = controller.get_user_by_oauth_id(oauth_id=user_data.get("sub"))
    if user:
        return user
    raise credentials_exception


