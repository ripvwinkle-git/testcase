
from uuid import UUID
from datetime import datetime
from typing import Annotated, Union
from fastapi import FastAPI, Depends, Query, Path
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(
    "/new",
    status_code = 201,
    response_model = schemas.RecordBase
)
def post_new(
    text: Annotated[str, Query(max_length=16)],
    db: Session = Depends(get_db)
):
    record = schemas.RecordCreate(text=text)
    return crud.create_record(db=db, record=record)

@app.get("/", response_model=None)
def get_root():
    return None

@app.get(
    "/all",
    response_model = list[schemas.RecordBase]
)
def get_all(db: Session = Depends(get_db)):
    records = crud.get_all_records(db)
    return records

@app.get(
    "/by_filters",
    response_model = list[schemas.RecordBase]
)
def get_by_filters(
    op: Annotated[str, Query(pattern=r'==|!=|>|<|>=|<=')],
    value: datetime,
    db: Session = Depends(get_db)
):
    '''
    op - оператор сравнения для фильтра;
    value - принимает дату и время.
    '''
    return crud.get_by_filters(db, field='timestamp', op=op, value=value)

@app.get(
    "/{count_uuid}",
    response_model = Union[
        list[schemas.RecordBase],
        schemas.RecordBase,
        None
    ]
)
def get_count_or_uuid(
    count_uuid: Union[
        UUID,
        Annotated[int, Path(ge=1)]
    ],
    db: Session = Depends(get_db)
):
    '''
    Если переданное значение uuid записи - возвращает запись с этим uuid;
    если переданное значение целое число - возвращает список с записями.
    '''
    if isinstance(count_uuid, UUID):
        return crud.get_uuid_record(db, uuid=count_uuid)
    return crud.get_records(db, count=count_uuid)

@app.get(
    "/{count}/{offset}",
    response_model = list[schemas.RecordBase]
)
def get_count_offset(
    offset: Annotated[int, Path(ge=0)],
    count: Annotated[int, Path(ge=1)],
    db: Session = Depends(get_db)
):
    records = crud.get_records(db, offset=offset, count=count)
    return records

@app.put(
    "/update/{uuid}",
    status_code = 201,
    response_model = schemas.RecordBase
)
def put_update(
    uuid: UUID,
    text: Annotated[str, Query(max_length=16)],
    db: Session = Depends(get_db)
):
    return crud.update_record(db=db, uuid=uuid, text=text)

@app.delete("/{uuid}")
def delete_record(
    uuid: UUID,
    db: Session = Depends(get_db)
):
    return crud.delete_record(db, uuid=uuid)
