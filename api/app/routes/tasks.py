from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.task_service import create_task, get_task
from ..database import get_db
from ..schemas import TaskCreate, TaskResponse
from uuid import UUID

router = APIRouter()

@router.post("/", response_model=TaskResponse)
async def create_new_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    new_task = await create_task(db, task.type, task.payload)
    return new_task

@router.get("/{task_id}", response_model=TaskResponse)
async def get_existing_task(task_id: str, db: AsyncSession = Depends(get_db)):
    task = await get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
