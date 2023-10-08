
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy_filters import apply_filters

from . import models, schemas

def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.RecordCreate(
        uuid=record.uuid,
        text=record.text,
        timestamp=record.timestamp
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_all_records(db: Session):
    return db.query(models.Record).all()

def get_uuid_record(db: Session, uuid: UUID):
    return db.query(models.Record).get(uuid)

def get_records(db: Session, count: int = 0, offset: int = 0):
    return db.query(models.Record).offset(offset).limit(count).all()

def get_by_filters(db: Session, field:str, op:str, value:str):
    filters = [{'field': field, 'op': op, 'value': value}]
    return apply_filters(db.query(models.RecordCreate), filters)

def update_record(db: Session, uuid: UUID, text: str):
    db.query(models.Record).filter(models.Record.uuid == uuid).\
    update({'text': text}, synchronize_session=False)
    db.commit()
    return db.query(models.Record).get(uuid)

def delete_record(db: Session, uuid: UUID):
    db.query(models.Record).filter(models.Record.uuid == uuid).\
    delete(synchronize_session=False)
    db.commit()
    return None
