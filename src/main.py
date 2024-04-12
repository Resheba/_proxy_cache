import os, sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from fastapi import FastAPI


async def lifespan(app: FastAPI):
    print('Start')
    yield
    print('End')


app = FastAPI(
    title="VacProxy",
    lifespan=lifespan
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('src.main:app', host='0.0.0.0', port=80, reload=True)
