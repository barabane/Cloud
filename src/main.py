from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.routes.UserRouter import user_router


@asynccontextmanager
async def lifespan(_):
    yield


app = FastAPI(title='Fast API', lifespan=lifespan)

app.include_router(user_router)
