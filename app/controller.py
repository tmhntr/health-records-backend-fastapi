from sqlalchemy.orm import Session
from sqlalchemy import select

from .models import User, HealthRecord, ProblemRecord


from . import models, schemas


def get_user(db: Session, user_id: int) -> User:
    result = db.scalars(select(User).where(User.id == user_id))
    return result.first()

    # return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User:
    result = db.scalars(select(User).where(User.email == email))
    return result.first()
    # return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.scalars(select(User).order_by(User.id).offset(skip).limit(limit)).all()


def create_user(db: Session, user: schemas.UserCreate) -> User:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_records(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[HealthRecord]:
    result = db.scalars(select(HealthRecord).where(HealthRecord.owner_id == user_id).order_by(HealthRecord.id).offset(skip).limit(limit))
    return result.all()


def create_user_record(db: Session, record: schemas.RecordCreate, user_id: int) -> HealthRecord:
    db_record = models.HealthRecord(**record.dict(), owner_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record