import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    'email, password, status',
    [
        ('test@example.com', 'test123', 200),
        (
            'barabayne@gmail.com',
            '$pbkdf2-sha256$29000$e88ZI2SMcQ7hfK.11lqrNQ$G2v5pHRv.NcFdAATtlsESe85XSKXALJNsRTylDbVOq8',
            409,
        ),
    ],
)
async def test_register_user(
    async_client: AsyncClient, email, password, status
) -> None:
    response = await async_client.post(
        '/users/register', params={'email': email, 'password': password}
    )

    assert response.status_code == status


@pytest.mark.parametrize(
    'email, password, status',
    [('test@example.com', 'test123', 404), ('barabayne@gmail.com', 'z2376844251', 200)],
)
async def test_login_user(async_client: AsyncClient, email, password, status) -> None:
    response = await async_client.post(
        '/users/login', params={'email': email, 'password': password}
    )

    assert response.status_code == status
