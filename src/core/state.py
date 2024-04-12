from typing import TypedDict

from .http_client import ParserClient


class State(TypedDict):
    client: ParserClient
