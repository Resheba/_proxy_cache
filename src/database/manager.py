from alchemynger import AsyncManager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import Settings


manager: AsyncManager = AsyncManager(Settings.DB_DSN)


async def SessionDepend() -> AsyncGenerator[AsyncSession, None]:
    async with manager.get_session() as session:
        yield session
        