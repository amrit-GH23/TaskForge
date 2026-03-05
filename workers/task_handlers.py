import asyncio

async def sleep_task(payload):
    duration = payload.get("duration", 1)
    await asyncio.sleep(duration)
    return {"message": f"Slept for {duration} seconds"}

async def math_task(payload):
    a = int(payload.get("a", 0))
    b = int(payload.get("b", 0))
    result = a + b
    return {"result": result}

TASK_HANDLERS = {
    "sleep": sleep_task,
    "math": math_task,
}
