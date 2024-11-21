from fastapi import FastAPI
from app.routers.task import router as task_router
from app.routers.user import router as user_router
import asyncio
from .backend.db import engine, Base
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Taskmanager"}

# Подключаем маршруты
app.include_router(task_router)
app.include_router(user_router)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Инициализация базы данных при запуске
if __name__ == "__main__":
    asyncio.run(init_db())