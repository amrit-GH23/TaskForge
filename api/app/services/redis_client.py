import redis.asyncio as redis
from ..config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


QUEUE_NAME = "task_queue"

async def enqueue_task(task_id:str):
    await redis_client.lpush(QUEUE_NAME,task_id)

    