import asyncio
import json

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import insert

from config import settings
from main import app
from src.database.database import Base, async_session_maker, engine
from src.database.models.FileModel import File
from src.database.models.SubscriptionModel import Subscription
from src.database.models.UserModel import User


@pytest.fixture(scope='function', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'mocks/mock_{model}.json', encoding='utf-8') as file:
            return json.load(file)

    subscriptions = open_mock_json('subscriptions')
    users = open_mock_json('users')
    files = open_mock_json('files')

    async with async_session_maker() as session:
        for model, values in [
            (Subscription, subscriptions),
            (User, users),
            (File, files),
        ]:
            query = insert(model).values(values)
            await session.execute(query)
        await session.commit()


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=settings.TEST_API_URL_ADDRESS
    ) as client:
        yield client


@pytest.fixture(scope='session')
async def authenticated_async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=settings.TEST_API_URL_ADDRESS
    ) as ac:
        response = await ac.post(
            '/users/login',
            params={
                'email': 'barabayne@gmail.com',
                'password': 'z2376844251',
            },
        )
        assert response.status_code == 200
        assert ac.cookies['auth_token']
        yield ac
