
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import Annotated
from pydantic import BaseModel, Field

class RecordBase(BaseModel):
    uuid: Annotated[UUID, Field(default_factory=uuid4)]
    text: Annotated[str, Field(max_length=16)]

class RecordCreate(RecordBase):
    timestamp: Annotated[
        datetime,
        Field(default_factory=lambda: datetime.now(timezone.utc))
    ]
