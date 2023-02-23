from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, Response, status

from app import models, schemas
from app.auth import VerifyToken, token_auth_scheme
from app.database import SessionLocal
from app.log import logger



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(response: Response, db: Session = Depends(get_db), token: str = Depends(token_auth_scheme)) -> schemas.TokenData:
    result = VerifyToken(token.credentials).verify()  # 👈 updated code

    # 👇 new code
    if result.get("status"):
       response.status_code = status.HTTP_400_BAD_REQUEST
       return result
    # 👆 new code
 
    return result


async def get_current_user(user_data: schemas.TokenData = Depends(authenticate_user), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Session"},
    )
    user = db.query(models.User).filter(models.User.email == user_data.get("email")).first()
    if user:
        return user
    raise credentials_exception


