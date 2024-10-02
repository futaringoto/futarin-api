import pytest
import starlette.status


@pytest.mark.asyncio
async def test_create_and_read(async_client):
    response = await async_client.post("/v2/users/", json={"raspi_id": 1})
    assert response.status_code == starlette.status.HTTP_200_OK
    response_obj = response.json()
    assert response_obj["raspi_id"] == 1
