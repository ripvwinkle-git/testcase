
from sqlalchemy import Column, String, UUID, DateTime

from .database import Base

class Record(Base):
    __tablename__ = 'gideone'
    uuid = Column(UUID, primary_key=True, index=True)
    text = Column(String(16))

class RecordCreate(Record):
    timestamp = Column(DateTime)
