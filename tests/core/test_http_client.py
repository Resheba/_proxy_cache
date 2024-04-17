import pytest

from src.core.http_client import ParserClient


@pytest.fixture
def client():
    return ParserClient()


def test_parser_client(client: ParserClient):
    assert client


@pytest.mark.asyncio
async def test_get_data(client: ParserClient):
    assert await client.get_data('https://jsonplaceholder.typicode.com/posts/1')
