from fastapi import APIRouter, Request, BackgroundTasks

from src.core import BaseResponse, ParserClient
from .tasks import reset_db


router = APIRouter()


@router.get("",
            response_model=BaseResponse[None],
            summary="Reset database",
            response_model_exclude_none=True,
            )
async def get(
    request: Request,
    background_tasks: BackgroundTasks,
):
    client: ParserClient = request.state.client
    background_tasks.add_task(reset_db, client)
    return BaseResponse(data=None)
