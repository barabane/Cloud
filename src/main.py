from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.middlewares import AuthMiddleware
from src.routes.FileRouter import file_router
from src.routes.UserRouter import user_router


@asynccontextmanager
async def lifespan(_):
    yield


app = FastAPI(title='Fast API', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.add_middleware(AuthMiddleware, prefixes=[file_router.prefix])

app.include_router(user_router)
app.include_router(file_router)
