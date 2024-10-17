import pytest
import starlette.status


@pytest.fixture(scope="session")
async def raspi_fixture(async_client):
    raspi_1 = await async_client.post("/v2/raspis", json={"name": "raspi_1"})
    assert raspi_1.status_code == starlette.status.HTTP_200_OK
    raspi_2 = await async_client.post("/v2/raspis", json={"name": "raspi_2"})
    assert raspi_2.status_code == starlette.status.HTTP_200_OK
    return [raspi_1.json(), raspi_2.json()]


@pytest.fixture(scope="session")
async def user_fixture(async_client, raspi_fixture):
    user_1 = await async_client.post(
        "/v2/users", json={"raspi_id": raspi_fixture[0]["id"], "name": "user_1"}
    )
    assert user_1.status_code == starlette.status.HTTP_200_OK
    user_2 = await async_client.post(
        "/v2/users", json={"raspi_id": raspi_fixture[1]["id"], "name": "user_2"}
    )
    assert user_2.status_code == starlette.status.HTTP_200_OK
    return [user_1.json(), user_2.json()]


@pytest.fixture(scope="session")
async def couple_fixture(async_client, user_fixture):
    couple_1 = await async_client.post(
        "/v2/couples",
        json={
            "user1_id": user_fixture[0]["id"],
            "user2_id": user_fixture[1]["id"],
            "name": "couple_1",
        },
    )
    assert couple_1.status_code == starlette.status.HTTP_200_OK
    return couple_1.json()
