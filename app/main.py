from fastapi import FastAPI
from routers.task import router as task_router
from routers.user import router as user_router
import asyncio
from app.backend.db import engine, Base

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