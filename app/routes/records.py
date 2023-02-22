from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from app import schemas, controller, models
from app.dependencies import get_current_user, get_db


router = APIRouter(
    prefix="/records",
    tags=["records", "health records", "health", "medical records"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Record)
def create_record(record: schemas.RecordCreate, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_record = controller.create_user_record(db=db, record=record, user_id=user.id)
    return schemas.Record.from_orm(db_record)

@router.delete("/{record_id}", response_model=schemas.Record)
def delete_record(record_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_record = controller.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if db_record.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(db_record)
    db.commit()
    return schemas.Record.from_orm(db_record)

@router.get("/", response_model=list[schemas.Record])
def read_records(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    records = controller.get_records(db, skip=skip, limit=limit, user_id=user.id)
    return [schemas.Record.from_orm(record) for record in records]


@router.get("/{record_id}", response_model=schemas.Record)
def read_record(record_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_record = controller.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if db_record.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return schemas.Record.from_orm(db_record)
    


