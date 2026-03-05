import asyncio
from sqlalchemy import select,update
from database import AsyncSessionLocal
from redis_client import get_task_from_queue
from models import Task
from task_handlers import TASK_HANDLERS

MAX_RETRIES = 3

async def process_task(task_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        if not task:
            print(f"Task {task_id} not found")
            return

        handler = TASK_HANDLERS.get(task.type)
        if not handler:
            print(f"No handler for task type {task.type}")
            return

        try:
            task.status = "RUNNING"
            await session.commit()

            result = await handler(task.payload)

            task.status = "completed"
            task.result = result
            await session.commit()
        except Exception as e:
            print(f"Error processing task {task_id}: {e}")
            task.retry_count += 1
            if task.retry_count >= MAX_RETRIES:
                task.status = "failed"
            else:
                task.status = "pending"
            await session.commit()

async def worker_loop():
    while True:
        task_id = await get_task_from_queue()
        await process_task(task_id)

if __name__ == "__main__":
    asyncio.run(worker_loop())