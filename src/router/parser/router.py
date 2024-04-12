from fastapi import APIRouter

from src.core import BaseResponse


router = APIRouter()


@router.get("/",
            response_model=BaseResponse[dict]
            )
async def get():
    return BaseResponse(data={'test': 'parser'})
