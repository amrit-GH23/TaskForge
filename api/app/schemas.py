from pydantic import BaseModel
from typing import Dict, Any, Optional
from uuid import UUID

class TaskCreate(BaseModel):
    type: str
    payload: Dict[str, Any] 

class TaskResponse(BaseModel):
    id: UUID
    status: str
    result: Optional[Dict[str, Any]] = None

    retry_count: int

    model_config = {
        "orm_mode": True
    }

