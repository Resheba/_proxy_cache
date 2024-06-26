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
from src.database import manager


async def lifespan(app: FastAPI) -> AsyncIterator[State]:
    await manager.connect(create_all=False, expire_on_commit=False)
    client: ParserClient = ParserClient()

    async with manager.get_session() as session:
        await session.run_sync(lambda sess: manager.Base.metadata.reflect(sess.connection(), views=True))

        from src.router.search.models import DataORM
        if DataORM.name not in manager.Base.metadata.tables:
            from src.router.database.tasks import reset_db
            await reset_db(client=client)

        from src.router.database.models import WorkPlaceColumnORM, ClientColumnORM, ProfessionColumnORM
        await session.run_sync(lambda sess: manager.Base.metadata.create_all(sess.connection(), tables=[WorkPlaceColumnORM.__table__, ClientColumnORM.__table__, ProfessionColumnORM.__table__]))

        await session.commit()
    
    from src.router import PaserRouter, SearchRouter, MvsRouter
    app.include_router(PaserRouter, prefix="/data")
    app.include_router(MvsRouter, prefix="/entities")
    app.include_router(SearchRouter, prefix="/search", tags=["Search"])

    yield State(client=client)


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
