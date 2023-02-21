from sqlalchemy.orm import Session
from sqlalchemy import select

from . import models, schemas
from app.utils import get_password_hash


def get_user(db: Session, user_id: int) -> models.User:
    result = db.scalars(select(models.User).where(models.User.id == user_id))
    return result.first()

    # return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    result = db.scalars(select(models.User).where(models.User.email == email))
    return result.first()
    # return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.scalars(select(models.User).order_by(models.User.id).offset(skip).limit(limit)).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_records(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[models.HealthRecord]:
    result = db.scalars(select(models.HealthRecord).where(
        models.HealthRecord.owner_id == user_id).order_by(models.HealthRecord.id).offset(skip).limit(limit))
    return result.all()


def create_user_record(db: Session, record: schemas.RecordCreate, user_id: int) -> models.HealthRecord:
    db_record = models.HealthRecord(**record.dict(), owner_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record
