from typing import Annotated
from fastapi import APIRouter, Query, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.core import BaseResponse, PaginatorPage
from src.database import SessionDepend


router = APIRouter()


from .repos import DataRepository


@router.get("",
    response_model=BaseResponse[list[dict]],
    summary="Search",
    )
async def search(
    *,
    request: Request,
    query: Annotated[str, Query(
        examples=[
            'ашан казань',
            'комплектовщик озон',
            'склад'
            ])] = None,
    session: Annotated[AsyncSession, Depends(SessionDepend)],
    paginator: Annotated[PaginatorPage, Depends()]
):
    params = {param: value for param, value in request.query_params.items() if param not in ('query', 'page_size', 'page_num')}
    print(params)
    data: list = await DataRepository(session).get(
        query=query, 
        offset=(paginator.page_num - 1) * paginator.page_size, 
        limit=paginator.page_size,
        **params
    )
    return BaseResponse(data=data)
