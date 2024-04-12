from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Request, BackgroundTasks, Depends

from src.core import BaseResponse, ParserClient
from src.database import SessionDepend

from .repos import ClientColumnRepository, ProfessionColumnRepository, WorkPlaceColumnRepository
from .tasks import reset_db


router = APIRouter()


@router.get("/reset",
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


@router.get("/client-columns",
            response_model=BaseResponse,
            summary="Get client columns",
            response_model_exclude_none=True,
            )
async def get_client_columns(
    session: Annotated[AsyncSession, Depends(SessionDepend)],
):
    columns: list[str] = await ClientColumnRepository(session).get(only_columns=['column_name'])
    print(columns)
    return BaseResponse(data=columns)
