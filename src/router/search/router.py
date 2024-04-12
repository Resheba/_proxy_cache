from typing import Annotated
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import BaseResponse, BaseHTTPException, PaginatorPage
from src.database import SessionDepend


router = APIRouter()


from .repos import DataRepository


@router.get("",
    response_model=BaseResponse[list[dict]],
    summary="Search",
    )
async def search(
    query: Annotated[str, Query(
        examples=[
            'ашан казань',
            'комплектовщик озон',
            'склад'
            ]
        )],
    session: Annotated[AsyncSession, Depends(SessionDepend)],
    paginator: Annotated[PaginatorPage, Depends()]
):
    data: list = await DataRepository(session).get(
        query=query, 
        offset=(paginator.page_num - 1) * paginator.page_size, 
        limit=paginator.page_size
    )
    return BaseResponse(data=data)
