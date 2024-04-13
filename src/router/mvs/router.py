from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Body, Depends

from src.core import BaseResponse, PaginatorPage
from src.database import SessionDepend

from .repos import ClientsRepository, WorkPlaceRepository, ProfessionsRepository


router = APIRouter()


@router.get("/clients",
    tags=["Client"],
    response_model=BaseResponse[list[dict]],
    response_model_exclude_none=True,
)
async def get_clients(
    session: Annotated[AsyncSession, Depends(SessionDepend)],
    paginator: Annotated[PaginatorPage, Depends()],
):
    data = await ClientsRepository(session).get(
        offset=(paginator.page_num - 1) * paginator.page_size, 
        limit=paginator.page_size,
        )
    return BaseResponse(data=data)


@router.get("/workplace",
    tags=["Workplace"],
    response_model=BaseResponse[list[dict]],
    response_model_exclude_none=True,
)
async def get_workplace(
    session: Annotated[AsyncSession, Depends(SessionDepend)],
    paginator: Annotated[PaginatorPage, Depends()],
):
    data = await WorkPlaceRepository(session).get(
        offset=(paginator.page_num - 1) * paginator.page_size, 
        limit=paginator.page_size,
        )
    return BaseResponse(data=data)


@router.get("/professions",
    tags=["Profession"],
    response_model=BaseResponse[list[dict]],
    response_model_exclude_none=True,
)
async def get_professions(
    session: Annotated[AsyncSession, Depends(SessionDepend)],
    paginator: Annotated[PaginatorPage, Depends()],
):
    data = await ProfessionsRepository(session).get(
        offset=(paginator.page_num - 1) * paginator.page_size, 
        limit=paginator.page_size,
        )
    return BaseResponse(data=data)


# @router.patch("/clients",
#     response_model=BaseResponse[str],
#     response_model_exclude_none=True,
# )
# async def replace_clients(
#     # stmt: Annotated[str, Body()],
#     session: Annotated[AsyncSession, Depends(SessionDepend)],
# ):
#     stmt: str = await ClientsRepository(session).replace()
#     return BaseResponse(data=stmt)
