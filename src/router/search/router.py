from typing import Annotated
from fastapi import APIRouter, Query, Depends, Request, Form
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
    data: list = await DataRepository(session).get(
        query=query, 
        offset=(paginator.page_num - 1) * paginator.page_size, 
        limit=paginator.page_size,
        **params
    )
    return BaseResponse(data=data)


@router.post("",
    response_model=BaseResponse[list[dict]],
    summary="Search by form-data",
    )
async def search_by_form_data(
    *,
    request: Request,
    query: Annotated[str, Form(alias='searching', validation_alias='searching')] = None,
    clientid: Annotated[int, Form()] = None,
    placeid: Annotated[int, Form()] = None,
    profid: Annotated[int, Form()] = None,
    session: Annotated[AsyncSession, Depends(SessionDepend)],
    paginator: Annotated[PaginatorPage, Depends()]
):
    # forms = dict(await request.form())
    all_filters: dict[str, int] = dict(clientid=clientid, placeid=placeid, profid=profid)
    filters: dict[str, int] = {key: value for key, value in all_filters.items() if value is not None}
    data: list = await DataRepository(session).get(
        query=query,  
        offset=(paginator.page_num - 1) * paginator.page_size, 
        limit=paginator.page_size,
        **filters,
    )
    return BaseResponse(data=data)