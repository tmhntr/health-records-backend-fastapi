from sqlalchemy.orm import Session
from sqlalchemy import select, update

from src.resources.record import model, schemas
from src.utils import validate_user

class RecordController:
    def __init__(self, db: Session):
        self.db = db

    def create_record(self, token, record: schemas.RecordCreate) -> schemas.Record:
        auth = validate_user(token)
        db_record = model.HealthRecord(**record.dict(), owner_id=auth.get("sub"))
        self.db.add(db_record)
        self.db.commit()
        self.db.refresh(db_record)
        return schemas.Record.from_orm(db_record)

    def get_records(self, token, skip: int = 0, limit: int = 100, sort_by: str = None, sort_dir: str = None, filter: str = None) -> list[schemas.Record]:
        auth = validate_user(token)


        stmt = select(model.HealthRecord).where(
            model.HealthRecord.owner_id == auth.get("sub"))
            
        if filter:
            for key, value in filter.items():
                stmt = stmt.where(getattr(model.HealthRecord, key) == value)

        if sort_by:
            if sort_dir == "desc":
                stmt = stmt.order_by(getattr(model.HealthRecord, sort_by).desc())
            else:
                stmt = stmt.order_by(getattr(model.HealthRecord, sort_by))
        else:
            stmt = stmt.order_by(model.HealthRecord.id)

        stmt = stmt.offset(skip).limit(limit)

        records = self.db.scalars(stmt).all()
        return [schemas.Record.from_orm(record) for record in records]

    def get_record(self, token, record_id: int) -> schemas.Record:
        auth = validate_user(token)

        record = self.db.scalars(select(model.HealthRecord).where(
            model.HealthRecord.id == record_id, model.HealthRecord.owner_id == auth.get("sub"))).first()
        return schemas.Record.from_orm(record)

    def update_record(self, token, record: schemas.RecordUpdate, record_id: int) -> schemas.Record:
        auth = validate_user(token)

        stmt = update(model.HealthRecord).where(
            model.HealthRecord.id == record_id, model.HealthRecord.owner_id == auth.get("sub")).values(**record.dict(exclude_unset=True))
        self.db.execute(stmt)
        self.db.commit()
        return self.get_record(token, record_id)

    def delete_record(self, token,  record_id: int) -> schemas.Record:
        auth = validate_user(token)

        record = self.get_record(token, record_id)
        if record.owner_id != auth.get("sub"):
            raise Exception("User does not have permission to delete this record")

        result = self.db.scalars(select(model.HealthRecord).where(
            model.HealthRecord.id == record_id, model.HealthRecord.owner_id == auth.get("sub")))
        self.db.delete(result.first())
        self.db.commit()

        return record

    def get_record_count(self, token) -> int:
        records = self.get_records(token, limit=None)
        return schemas.RecordCount(count=len(records))

