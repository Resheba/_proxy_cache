from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Body, Request, BackgroundTasks, Depends, Query

from src.core import BaseResponse, ParserClient
from src.database import SessionDepend

from .repos import ClientColumnRepository, ProfessionColumnRepository, WorkPlaceColumnRepository
from .schemas import ColumnReturn
from .tasks import reset_db

from ..mvs.repos import ClientsRepository, WorkPlaceRepository


router = APIRouter()


@router.patch("/reset",
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
            response_model=BaseResponse[list[str]],
            summary="Get client columns",
            response_model_exclude_none=True,
            )
async def get_client_columns(
    session: Annotated[AsyncSession, Depends(SessionDepend)],
):
    columns: list[str] = await ClientColumnRepository(session).get(only_columns=['column_name'])
    return BaseResponse(data=columns)


@router.patch("/client-columns",
            response_model=BaseResponse[list[str]],
            summary="Create client columns",
            response_model_exclude_none=True,
            )
async def create_client_columns(
    column_names: Annotated[list[str], Body(min_length=1, embed=True)],
    session: Annotated[AsyncSession, Depends(SessionDepend)],
):
    repo: ClientColumnRepository = ClientColumnRepository(session)
    await repo.delete()
    columns: list = await repo.create([ColumnReturn(column_name=column_name) for column_name in column_names])
    await ClientsRepository(session).replace()

    return BaseResponse(data=[column.column_name for column in columns])



@router.get("/workplace-columns",
            response_model=BaseResponse[list[str]],
            summary="Get workplace columns",
            response_model_exclude_none=True,
            )
async def get_workplace_columns(
    session: Annotated[AsyncSession, Depends(SessionDepend)],
):
    columns: list[str] = await WorkPlaceColumnRepository(session).get(only_columns=['column_name'])
    return BaseResponse(data=columns)


@router.patch("/workplace-columns",
            response_model=BaseResponse[list[str]],
            summary="Create workplace columns",
            response_model_exclude_none=True,
            )
async def create_workplace_columns(
    column_names: Annotated[list[str], Body(min_length=1, embed=True)],
    session: Annotated[AsyncSession, Depends(SessionDepend)],
):
    repo: WorkPlaceColumnRepository = WorkPlaceColumnRepository(session)
    await repo.delete()
    columns: list = await repo.create([ColumnReturn(column_name=column_name) for column_name in column_names])
    await WorkPlaceRepository(session).replace()

    return BaseResponse(data=[column.column_name for column in columns])


# @router.post("/workplace-columns",
#             response_model=BaseResponse[ColumnReturn],
#             summary="Create workplace columns",
#             response_model_exclude_none=True,
#             )
# async def create_workplace_columns(
#     column_name: Annotated[str, Body(min_length=1, embed=True)],
#     session: Annotated[AsyncSession, Depends(SessionDepend)],
# ):
#     column = await WorkPlaceColumnRepository(session).create(ColumnReturn(column_name=column_name))
#     # TODO refuse matview logic
#     return BaseResponse(data=column)


# @router.delete("/workplace-columns",
#             response_model=BaseResponse[None],
#             summary="Delete workplace columns",
#             response_model_exclude_none=True,
#             )
# async def delete_workplace_columns(
#     ids: Annotated[list[int], Query(alias='id')],
#     session: Annotated[AsyncSession, Depends(SessionDepend)],
# ):
#     await WorkPlaceColumnRepository(session).delete(ids)
#     # TODO refuse matview logic
#     return BaseResponse(data=None)


# @router.get("/profession-columns",
#             response_model=BaseResponse[list[ColumnReturn]],
#             summary="Get profession columns",
#             response_model_exclude_none=True,
#             )
# async def get_profession_columns(
#     session: Annotated[AsyncSession, Depends(SessionDepend)],
# ):
#     columns: list = await ProfessionColumnRepository(session).get()
#     return BaseResponse(data=columns)


# @router.post("/profession-columns",
#             response_model=BaseResponse[ColumnReturn],
#             summary="Create profession columns",
#             response_model_exclude_none=True,
#             )
# async def create_profession_columns(
#     column_name: Annotated[str, Body(min_length=1, embed=True)],
#     session: Annotated[AsyncSession, Depends(SessionDepend)],
# ):
#     column = await ProfessionColumnRepository(session).create(ColumnReturn(column_name=column_name))
#     # TODO refuse matview logic
#     return BaseResponse(data=column)


# @router.delete("/profession-columns",
#             response_model=BaseResponse[None],
#             summary="Delete profession columns",
#             response_model_exclude_none=True,
#             )
# async def delete_profession_columns(
#     ids: Annotated[list[int], Query(alias='id')],
#     session: Annotated[AsyncSession, Depends(SessionDepend)],
# ):
#     await ProfessionColumnRepository(session).delete(ids)
#     # TODO refuse matview logic
#     return BaseResponse(data=None)
