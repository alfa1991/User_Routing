import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Создаём движок для работы с SQLite
DATABASE_URL = "sqlite+aiosqlite:///taskmanager.db"
engine = create_async_engine(DATABASE_URL, echo=True)

# Создаём фабрику для сессий
SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Базовый класс для моделей
class Base(DeclarativeBase):
    pass

# Создание таблиц асинхронно
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Для использования с asyncio.run()
def main():
    asyncio.run(create_tables())

if __name__ == "__main__":
    main()