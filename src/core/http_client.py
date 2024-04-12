from httpx import AsyncClient, Response

from .exception import BaseHTTPException


class ParserClient:
    def __init__(self) -> None:
        self.client = AsyncClient()

    def reload(self) -> None:
        self.client = AsyncClient()

    async def get_data(self, url: str, **kwargs) -> Response:
        response: Response = await self.client.get(url, **kwargs)
        if response.status_code != 200:
            raise BaseHTTPException(status_code=response.status_code, msg=response.text)
        return response
    