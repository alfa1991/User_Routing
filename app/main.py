from fastapi import FastAPI
from app.routers.task import router as task_router
from app.routers.user import router as user_router
import asyncio
from .backend.db import engine, Base, SessionLocal
from app.models.task import Task
from app.models.user import User
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Taskmanager"}

# Подключаем маршруты
app.include_router(task_router)
app.include_router(user_router, prefix="/user", tags=["user"])

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_data():
    async with SessionLocal() as session:
        # Получаем все задачи и пользователей асинхронно
        result_tasks = await session.execute(Task.__table__.select())
        tasks = result_tasks.scalars().all()

        result_users = await session.execute(User.__table__.select())
        users = result_users.scalars().all()

        print("Tasks:", tasks)
        print("Users:", users)


# Инициализация базы данных при запуске
if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(get_data())
