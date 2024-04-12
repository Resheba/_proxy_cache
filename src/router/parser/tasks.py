from logging import info
from httpx import Response
from pandas import DataFrame

from src.core import ParserClient
from src.config import Settings


async def reset_db(client: ParserClient) -> None:
    response: Response = await client.get_data(url=Settings.BASE_URL)
    data: list[dict] = response.json()
    df: DataFrame = DataFrame(data)
    df.to_sql('data', con=Settings.DB_SYNC_DSN, if_exists='replace', index=False)
    info('Database reset')