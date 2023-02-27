from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session


from .. import controllers, schemas, dependencies, env

import logging
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/users",
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=schemas.User)
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
    controller = controllers.UserController(db)

    if user.key != env.env.get("USER_REGISTRATION_KEY"):
        raise HTTPException(status_code=403, detail="Forbidden")

    db_user = controller.get_user_by_email(email=user.email)
    
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    db_user =  controller.get_user_by_oauth_id(oauth_id=user.oauth_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    db_user = controller.create_user(user=user)
    return schemas.User.from_orm(db_user)


@router.get("", response_model=list[schemas.User])
@router.get("/", response_model=list[schemas.User])
def read_users(skip: int = 0, token_data: schemas.TokenData = Depends(dependencies.authenticate_user), limit: int = 100, db: Session = Depends(dependencies.get_db)):
    controller = controllers.UserController(db)


    users = controller.get_users(skip=skip, limit=limit)
    return [schemas.User.from_orm(user) for user in users]

@router.get("/me", response_model=schemas.User)
@router.get("/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(dependencies.get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=schemas.User)
@router.get("/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    controller = controllers.UserController(db)
    db_user = controller.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.User.from_orm(db_user)


@router.put("/{user_id}", response_model=schemas.User)
@router.put("/{user_id}/", response_model=schemas.User)
def update_user(user_id: int, user: schemas.User, db: Session = Depends(dependencies.get_db)):
    controller = controllers.UserController(db)
    db_user = controller.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user = controllers.update_user(db=db, user=user, user_id=user_id)
    return schemas.User.from_orm(db_user)


@router.delete("/{user_id}", response_model=schemas.User)
@router.delete("/{user_id}/", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db)):
    controller = controllers.UserController(db)
    db_user = controller.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return schemas.User.from_orm(db_user)




