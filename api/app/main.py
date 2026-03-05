from fastapi import FastAPI
from .routes.tasks import router as tasks_router
from .database import engine, Base

app=FastAPI()

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        