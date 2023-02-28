from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from src import dependencies


from src.resources.user.controller import UserController
from src.resources.user import schemas

import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=schemas.User)
@router.post("/", response_model=schemas.User)
def create_user(data: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    controller = UserController(db)
    return controller.create_user(data=data)


@router.get("", response_model=list[schemas.User])
@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, token = Depends(dependencies.oauth2_scheme), limit: int = 100, db: Session = Depends(dependencies.get_db)):
    controller = UserController(db)
    return controller.get_users(token, skip=skip, limit=limit)

@router.get("/me", response_model=schemas.User)
@router.get("/me/", response_model=schemas.User)
async def read_users_me(token = Depends(dependencies.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    controller = UserController(db)
    return controller.get_current_user(token=token)

@router.get("/{user_id}", response_model=schemas.User)
@router.get("/{user_id}/", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(dependencies.get_db), token: str = Depends(dependencies.oauth2_scheme)):
    controller = UserController(db)
    return controller.get_user(token, user_id=user_id)


@router.put("/{user_id}", response_model=schemas.User)
@router.put("/{user_id}/", response_model=schemas.User)
def update_user(user_id: str, user: schemas.User, token = Depends(dependencies.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    controller = UserController(db)
    return controller.update_user(token, user, user_id=user_id)


@router.delete("/{user_id}", response_model=schemas.User)
@router.delete("/{user_id}/", response_model=schemas.User)
def delete_user(user_id: str, token = Depends(dependencies.oauth2_scheme), db: Session = Depends(dependencies.get_db)):
    controller = UserController(db)
    return controller.delete_user(token, user_id=user_id)




