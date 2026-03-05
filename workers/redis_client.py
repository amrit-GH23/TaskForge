import redis.asyncio as redis
from config import settings

redis_client = redis.from_url(settings.REDIS_URL,decode_responses=True)

QUEUE_NAME = "task_queue"

async def get_task_from_queue():
    _,task_id= await redis_client.brpop(QUEUE_NAME)
    return task_id