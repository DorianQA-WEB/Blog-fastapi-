"""
Модуль для настройки асинхронного взаимодействия с базой данных с использованием SQLAlchemy 2.0+.

Включает в себя:
- Создание асинхронного движка базы данных.
- Настройку фабрики сессий для асинхронной работы.
- Инициализацию моделей (создание таблиц).

Используется в FastAPI-приложениях или других асинхронных фреймворках.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# URL базы данных (SQLite с асинхронным драйвером)
DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

# Асинхронный движок базы данных
# Параметр `echo=True` включает логирование SQL-запросов (удобно для отладки)
engine = create_async_engine((DATABASE_URL, echo=True))


# Базовый класс для всех моделей
# Наследуйте от этого класса, чтобы определить ORM-модели
class Base(DeclarativeBase):
    pass

# Фабрика асинхронных сессий
# Используется для получения сессий в обработчиках (например, через Depends в FastAPI)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
# Асинхронная функция для инициализации базы данных
async def create_db_and_tables():
    """
    Асинхронно создаёт все таблицы в базе данных, если они ещё не существуют.

    Использует метод `run_sync`, чтобы выполнить синхронную команду `create_all`
    в асинхронном контексте.

    Пример использования:
        await create_db_and_tables()

    Предупреждение:
        Не вызывайте эту функцию напрямую в production без проверки окружения.
        Обычно используется при старте приложения или в скриптах инициализации.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)