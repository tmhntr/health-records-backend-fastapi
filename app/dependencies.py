from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request, status

from app import models, schemas
from app.database import SessionLocal
from app.log import logger
# from app.auth import SECRET_KEY, ALGORITHM
# from app.controller import get_user_by_email
# from app.auth import oauth2_scheme


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(request: Request, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Session"},
    )
    logger.debug(request.session)
    user = request.session.get("user")
    logger.debug(user)
    if user:
        user = db.query(models.User).filter(models.User.email == user.get("email")).first()
        if user:
            return user
    raise credentials_exception

# async def get_current_user(user: models.User, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> models.User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         user = get_user_by_email(db, email=email)
#     except:
#         raise credentials_exception
#     return user


# def get_current_active_user(current_user: models.User = Depends(get_current_user)) -> models.User:
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
