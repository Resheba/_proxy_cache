from fastapi import APIRouter, Request
from httpx import Response

from src.core import BaseResponse, ParserClient
from src.config import Settings


router = APIRouter()


@router.get("",
            response_model=BaseResponse[list]
            )
async def get(
    request: Request
):
    client: ParserClient = request.state.client
    response: Response = await client.get_data(url=Settings.BASE_URL)
    data: list[dict] = response.json()
    return BaseResponse(data=data)
