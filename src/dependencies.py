from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, Response, status

# local imports
import src.schemas as schemas
from src.auth import VerifyToken, token_auth_scheme
from src.database import SessionLocal
from src.log import logger
from src.controllers import UserController



# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def authenticate_user(response: Response, token: str = Depends(token_auth_scheme)) -> schemas.TokenData:
    logger.debug(token)
    result = VerifyToken(token.credentials).verify() 
    logger.debug(result)
    if result.get("status"):
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result.get("msg") or "Could not validate credentials",
            headers={"WWW-Authenticate": "Session"},
        )
    return result


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


