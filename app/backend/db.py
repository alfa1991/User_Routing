from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.schema import CreateTable


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

