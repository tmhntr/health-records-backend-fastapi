from fastapi import Depends, APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from .. import schemas, controller, models, dependencies


get_current_user, get_db = dependencies.get_current_user, dependencies.get_db


router = APIRouter(
    prefix="/records",
    tags=["records", "health records", "health", "medical records"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=schemas.Record)
@router.post("/", response_model=schemas.Record)
async def create_record(record: schemas.RecordCreate, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_record = controller.create_user_record(
        db=db, record=record, user_id=user.id)
    return schemas.Record.from_orm(db_record)


@router.delete("/{record_id}", response_model=schemas.Record)
@router.delete("/{record_id}/", response_model=schemas.Record)
async def delete_record(record_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
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


@router.get("", response_model=list[schemas.Record])
@router.get("/", response_model=list[schemas.Record])
async def read_records(skip: int = 0, limit: int = 100, sort_by: str = None, sort_dir: str = None, filter: str = None, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    records = controller.get_records(
        db, user_id=user.id, skip=skip, limit=limit, sort_by=sort_by, sort_dir=sort_dir, filter=filter)
    return [schemas.Record.from_orm(record) for record in records]

@router.get("/count", response_model=schemas.Count)
@router.get("/count/", response_model=schemas.Count)
async def read_records_count(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    count = controller.get_records_count(db, user_id=user.id)
    return schemas.Count(count=count)


@router.get("/{record_id}", response_model=schemas.Record)
@router.get("/{record_id}/", response_model=schemas.Record)
async def read_record(record_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_record = controller.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if db_record.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return schemas.Record.from_orm(db_record)

@router.put("/{record_id}", response_model=schemas.Record)
@router.put("/{record_id}/", response_model=schemas.Record)
async def update_record(record_id: int, record: schemas.RecordUpdate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_record = controller.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    if db_record.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    for key, value in record.dict(exclude_unset=True).items():
        setattr(db_record, key, value)
    db_record = controller.update_record(db, db_record, record)
    return schemas.Record.from_orm(db_record)