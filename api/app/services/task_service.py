from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import Task
from .redis_client import enqueue_task

async def create_task(db:AsyncSession, task_type:str, payload:dict):
    new_task = Task(type=task_type, payload=payload)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    await enqueue_task(str(new_task.id))
    return new_task

async def get_task(db:AsyncSession, task_id:int):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()

