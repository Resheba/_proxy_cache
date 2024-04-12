from httpx import Response
from typing import Annotated
from pandas import DataFrame
from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection
from fastapi import APIRouter, Request, BackgroundTasks, Depends

from src.core import BaseResponse, ParserClient
from src.config import Settings
from src.database import SessionDepend


router = APIRouter()


@router.get("",
            response_model=BaseResponse[None]
            )
async def get(
    request: Request,
    background_tasks: BackgroundTasks,
):
    client: ParserClient = request.state.client
    response: Response = await client.get_data(url=Settings.BASE_URL)
    data: list[dict] = response.json()
    df: DataFrame = DataFrame(data)
    background_tasks.add_task(df.to_sql, 'data', con=Settings.DB_SYNC_DSN, if_exists='replace', index=False)
    return BaseResponse(data=None)
