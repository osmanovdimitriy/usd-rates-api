import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

load_dotenv()

# Берем твой URL из .env и меняем postgresql:// на postgresql+asyncpg://
DATABASE_URL = os.getenv("DATABASE_URL").replace("postgresql://", "postgresql+asyncpg://")

# Движок (подключение к БД)
engine = create_async_engine(DATABASE_URL)

# Фабрика сессий (через нее будем делать запросы)
async_session = async_sessionmaker(engine, expire_on_commit=False)

from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session