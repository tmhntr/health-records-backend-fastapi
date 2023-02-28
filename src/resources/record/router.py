from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from src import dependencies
from src.resources.record import schemas
from src.resources.record.controller import RecordController

get_db =  dependencies.get_db


router = APIRouter(
    prefix="/records",
    tags=["records", "health records", "health", "medical records"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=schemas.Record)
@router.post("/", response_model=schemas.Record)
async def create_record(record: schemas.RecordCreate, token = Depends(dependencies.oauth2_scheme), db: Session = Depends(get_db)):
    controller = RecordController(db)
    return controller.create_record(token, record=record)


@router.delete("/{record_id}", response_model=schemas.Record)
@router.delete("/{record_id}/", response_model=schemas.Record)
async def delete_record(record_id: int, token = Depends(dependencies.oauth2_scheme), db: Session = Depends(get_db)):
    controller = RecordController(db)
    return controller.delete_record(token, record_id=record_id)


@router.get("", response_model=list[schemas.Record])
@router.get("/", response_model=list[schemas.Record])
async def read_records(skip: int = 0, limit: int = 100, sort_by: str = None, sort_dir: str = None, filter: str = None, token = Depends(dependencies.oauth2_scheme), db: Session = Depends(get_db)):
    controller = RecordController(db)
    return controller.get_records(token, skip=skip, limit=limit, sort_by=sort_by, sort_dir=sort_dir, filter=filter)

@router.get("/count", response_model=schemas.RecordCount)
@router.get("/count/", response_model=schemas.RecordCount)
async def read_records_count(db: Session = Depends(get_db), token = Depends(dependencies.oauth2_scheme)):
    controller = RecordController(db)
    return controller.get_record_count(token)


@router.get("/{record_id}", response_model=schemas.Record)
@router.get("/{record_id}/", response_model=schemas.Record)
async def read_record(record_id: int, db: Session = Depends(get_db), token = Depends(dependencies.oauth2_scheme)):
    controller = RecordController(db)
    return controller.get_record(token, record_id=record_id)

@router.put("/{record_id}", response_model=schemas.Record)
@router.put("/{record_id}/", response_model=schemas.Record)
async def update_record(record_id: int, record: schemas.RecordUpdate, db: Session = Depends(get_db), token = Depends(dependencies.oauth2_scheme)):
    controller = RecordController(db)
    return controller.update_record(token, record=record, record_id=record_id)