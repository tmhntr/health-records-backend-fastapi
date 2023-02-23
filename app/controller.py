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


def get_records(db: Session, user_id: int, skip: int = 0, limit: int = 100, sort_by: str = None, sort_dir: str = None, filter: str = None) -> list[models.HealthRecord]:
    
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

def get_record(db: Session, record_id: int) -> models.HealthRecord:
    result = db.scalars(select(models.HealthRecord).where(models.HealthRecord.id == record_id))
    return result.first()

def create_user_record(db: Session, record: schemas.RecordCreate, user_id: int) -> models.HealthRecord:
    db_record = models.HealthRecord(**record.dict(), owner_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_record(db: Session, record: schemas.RecordUpdate, record_id: int) -> models.HealthRecord:
    db_record = get_record(db, record_id=record_id)
    if db_record is None:
        return None
    for key, value in record.dict(exclude_unset=True).items():
        setattr(db_record, key, value)
    db.commit()
    db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int) -> models.HealthRecord:
    db_record = get_record(db, record_id=record_id)
    if db_record is None:
        return None
    db.delete(db_record)
    db.commit()
    return db_record