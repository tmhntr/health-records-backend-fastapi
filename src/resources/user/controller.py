from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from src import utils

from src.resources.user import model, schemas
from src.utils import validate_user


class UserController:
    def __init__(self, db: Session):
        self.db = db

    
    def get_user(self, token, user_id) -> schemas.User:
        auth = validate_user(token)
        if auth.get("sub") != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        user = self.db.scalars(select(model.User).where(model.User.id == user_id)).first()
        return schemas.User.from_orm(user)


    def get_user_by_email(self, token, email: str) -> schemas.User:
        user = validate_user(token)
        user = self.db.scalars(select(model.User).where(model.User.email == email, model.User.id == user.get("sub"))).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return schemas.User.from_orm(user)

    def get_users(self, token, skip: int = 0, limit: int = 100) -> list[model.User]:
        user = validate_user(token)
        scopes = user.get("scope").split(" ")
        if "read:users" not in scopes:
            raise HTTPException(status_code=403, detail="Forbidden")

        try:
            users = self.db.scalars(select(model.User).order_by(model.User.id).offset(skip).limit(limit)).all()
            return [schemas.User.from_orm(user) for user in users]
        except:
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    def get_current_user(self, token) -> schemas.User:
        user = validate_user(token)
        user = self.db.scalars(select(model.User).where(model.User.id == user.get("sub"))).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return schemas.User.from_orm(user)

    def create_user(self, data: schemas.UserCreate) -> schemas.User:
        if data.key != utils.env_get("USER_REGISTRATION_KEY"):
            raise HTTPException(status_code=403, detail="Forbidden")

        db_user = self.db.scalar(select(model.User).where(model.User.email == data.email))
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        db_user = self.db.scalar(select(model.User).where(model.User.id == data.user_id))
        if db_user:
            raise HTTPException(status_code=400, detail="UserId already registered")

        try:
        # hashed_password = get_password_hash(user.password)
            db_user = model.User(id=data.user_id ,email=data.email)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update_user(self, token, user: schemas.UserUpdate, user_id) -> schemas.User:
        auth = validate_user(token)
        if auth.get("sub") != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        try:
            result = update(model.User).where(model.User.id == user_id).values(**user.dict(exclude_unset=True))
            self.db.execute(result)
            self.db.commit()
            return self.get_user(user_id)
        except:
            raise Exception("could not update user")

    def delete_user(self, token, user_id: int) -> schemas.User:
        auth = validate_user(token)
        if auth.get("sub") != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")

        try:
            result = self.db.scalars(select(model.User).where(model.User.id == user_id))
            user = result.first()
            self.db.delete(user)
            self.db.commit()
            return schemas.User.from_orm(user)
        except:
            raise Exception("could not delete user")
