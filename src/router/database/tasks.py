import json
from fastapi import File
from sqlalchemy import text
from httpx import Response
from pandas import DataFrame

from src.core import ParserClient, logger
from src.config import Settings
from src.database import manager

from .models import ClientColumnORM, ProfessionColumnORM, WorkPlaceColumnORM


async def reset_db(client: ParserClient, file: bytes) -> None:
    # response: Response | None = await client.get_data(url=Settings.BASE_URL)
    # if response is None:
    #     with open('data.json', encoding='utf-8') as file:
    #         data = json.load(file)
    # else:
    #     data: list[dict] = response.json()

    if file is not None:
        data = json.loads(file.decode('utf-8'))
    elif response := await client.get_data(url=Settings.BASE_URL):
        data = response.json()
    else:
        logger.warn('No data found')
        return

    df: DataFrame = DataFrame(data)
    async with manager.get_session() as session:
        await session.run_sync(lambda sess: manager.Base.metadata.reflect(sess.connection()))
        if 'data' in manager.Base.metadata.tables:
            await session.execute(text("DROP TABLE IF EXISTS data CASCADE"))
            await session.run_sync(lambda sess: [sess.execute(table.delete()) for table in manager.Base.metadata.tables.values() if table.name in (WorkPlaceColumnORM.__tablename__, ClientColumnORM.__tablename__, ProfessionColumnORM.__tablename__) ])
            await session.commit()
        df.to_sql('data', con=Settings.DB_SYNC_DSN, if_exists='replace', index=False)
        manager.Base.metadata.clear()
        await session.run_sync(lambda sess: manager.Base.metadata.reflect(sess.connection()))
    logger.info('Database reset')
