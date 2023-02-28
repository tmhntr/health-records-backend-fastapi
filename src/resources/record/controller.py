from sqlalchemy.orm import Session
from sqlalchemy import select, update

import src.models as models
import src.schemas as schemas

class RecordController:
    def __init__(self, db: Session):
        self.db = db

    def create_record(self, record: schemas.RecordCreate, user_id: int) -> models.HealthRecord:
        db_record = models.HealthRecord(**record.dict(), owner_id=user_id)
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

    def get_record_count(self, user_id: int) -> int:
        result = self.db.scalars(select(models.HealthRecord).where(
            models.HealthRecord.owner_id == user_id))
        return len(result.all())

