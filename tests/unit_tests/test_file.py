import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    'file_id, status',
    [
        ('ebb39ab4-1375-4408-923c-589fd7b66dd6', 200),
        ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 200),
    ],
)
async def test_get_file(file_id, status, authenticated_async_client: AsyncClient):
    response = await authenticated_async_client.get(f'files/{file_id}')

    assert response.status_code == status
    assert response.json() == []
