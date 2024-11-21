import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from sqlalchemy.orm import sessionmaker

# Добавляем корневую директорию в sys.path для доступа к проекту
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.backend.db import Base  # Импорт Base из вашего проекта

# Подключение к базе данных
engine = create_engine('sqlite:///C:/Users/Ilgiz Agliullin/PycharmProjects/pythonProject1/taskmanager.db')

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Получение конфигурации Alembic
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Указываем метаданные для автогенерации миграций
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Выбор режима работы: offline или online
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
