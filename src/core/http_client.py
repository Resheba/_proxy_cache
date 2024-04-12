from httpx import AsyncClient, Response

from .exception import BaseHTTPException


class ParserClient:
    def __init__(self, base_url: str) -> None:
        self.client = AsyncClient(base_url=base_url)

    def reload(self) -> None:
        self.client = AsyncClient(base_url=self.client.base_url)

    async def get_data(self, **kwargs) -> Response:
        response: Response = await self.client.get(**kwargs)
        if response.status_code != 200:
            raise BaseHTTPException(status_code=response.status_code, msg=response.text)
        return response
    