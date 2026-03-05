import uuid
from sqlalchemy import Column, String, JSON, DateTime, Integer
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type= Column(String, nullable=False)
    payload= Column(JSON, nullable=False)
    status= Column(String, nullable=False, default="pending")
    result= Column(JSON, nullable=True)
    retry_count= Column(Integer, nullable=False, default=0)
    created_at= Column(DateTime(timezone=True), server_default=func.now())
    updated_at= Column(DateTime(timezone=True), onupdate=func.now())