import pytest
import starlette.status


@pytest.fixture
@pytest.mark.asyncio
async def create_raspi(async_client):
    response = await async_client.post("/v2/raspis/", json={})
    assert response.status_code == starlette.status.HTTP_200_OK
    return response.json()


async def test_create_and_read(async_client, create_raspi):
    response = await async_client.post(
        "/v2/users/", json={"raspi_id": create_raspi["id"]}
    )
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["raspi_id"] == 1
