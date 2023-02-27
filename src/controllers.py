from sqlalchemy.orm import Session
from sqlalchemy import select, update

import src.models as models
import src.schemas as schemas

class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, user_id: int) -> models.User:
        try:
            result = self.db.scalars(select(models.User).where(models.User.id == user_id))
            return result.first()
        except:
            raise Exception("could not retrieve user")

    def get_user_by_email(self, email: str) -> models.User:
        try:
            result = self.db.scalars(select(models.User).where(models.User.email == email))
            return result.first()
        except:
            raise Exception("could not retrieve user")

    def get_user_by_oauth_id(self, oauth_id: str) -> models.User:
        try:
            result = self.db.scalars(select(models.User).where(models.User.oauth_id == oauth_id))
            return result.first()
        except:
            raise Exception("could not retrieve user")

    def get_users(self, skip: int = 0, limit: int = 100) -> list[models.User]:
        try:
            result = self.db.scalars(select(models.User).order_by(models.User.id).offset(skip).limit(limit))
            return result.all()
        except:
            raise Exception("could not retrieve users")

    def create_user(self, user: schemas.UserCreate) -> models.User:
        try:
        # hashed_password = get_password_hash(user.password)
            db_user = models.User(email=user.email, oauth_id=user.oauth_id)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except:
            raise Exception("could not create user")

class RecordController:
    def __init__(self, db: Session):
        self.db = db

    def create_record(self, record: schemas.RecordCreate, user_id: int) -> models.HealthRecord:
        db_record = models.Record(**record.dict(), owner_id=user_id)
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return db_record

    def get_records(self, user_id: int, skip: int = 0, limit: int = 100, sort_by: str = None, sort_dir: str = None, filter: str = None) -> list[models.HealthRecord]:
        db = self.db
        result = select(models.HealthRecord).where(
            models.HealthRecord.owner_id == user_id)
            
        if filter:
            for key, value in filter.items():
                result = result.where(getattr(models.HealthRecord, key) == value)

        if sort_by:
            if sort_dir == "desc":
                result = result.order_by(getattr(models.HealthRecord, sort_by).desc())
            else:
                result = result.order_by(getattr(models.HealthRecord, sort_by))
        else:
            result = result.order_by(models.HealthRecord.id)

        result = result.offset(skip).limit(limit)

        result = db.scalars(result)
        return result.all()

    def get_record(self, record_id: int, user_id: int) -> models.HealthRecord:
        result = self.db.scalars(select(models.HealthRecord).where(
            models.HealthRecord.id == record_id, models.HealthRecord.owner_id == user_id))
        return result.first()

    def update_record(self, record: schemas.RecordUpdate, record_id: int, user_id: int) -> models.HealthRecord:
        db = self.db
        result = update(models.HealthRecord).where(
            models.HealthRecord.id == record_id, models.HealthRecord.owner_id == user_id).values(**record.dict(exclude_unset=True))
        db.execute(result)
        db.commit()
        return self.get_record(record_id, user_id)

    def delete_record(self, record_id: int, user_id: int) -> None:
        db = self.db
        result = db.scalars(select(models.HealthRecord).where(
            models.HealthRecord.id == record_id, models.HealthRecord.owner_id == user_id))
        db.delete(result.first())
        db.commit()

