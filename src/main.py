import os, sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from fastapi import FastAPI
from typing import AsyncIterator

from src.core import (
    BaseHTTPException, 
    base_exception_handler,
    ParserClient,
    State
)
from src.router import PaserRouter


async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    app.include_router(PaserRouter, prefix="/parser")

    client: ParserClient = ParserClient()
    print('Start')
    yield State(client=client)
    print('End')


app = FastAPI(
    title="VacProxy",
    lifespan=lifespan,
    exception_handlers={
        BaseHTTPException: base_exception_handler,
    }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('src.main:app', host='0.0.0.0', port=80, reload=True)
