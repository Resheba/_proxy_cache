from httpx import Response
from pandas import DataFrame
from fastapi import APIRouter, Request, BackgroundTasks

from src.core import BaseResponse, ParserClient
from src.config import Settings
from .tasks import reset_db


router = APIRouter()


@router.get("",
            response_model=BaseResponse[None]
            )
async def get(
    request: Request,
    background_tasks: BackgroundTasks,
):
    client: ParserClient = request.state.client
    background_tasks.add_task(reset_db, client)
    return BaseResponse(data=None)
