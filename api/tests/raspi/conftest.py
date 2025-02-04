import pytest
import starlette.status


@pytest.fixture(scope="module")
async def raspi_fixture(async_client):
    raspi_1 = await async_client.post("/v2/raspis/", json={"name": "raspi_1"})
    assert raspi_1.status_code == starlette.status.HTTP_200_OK
    raspi_2 = await async_client.post("/v2/raspis/", json={"name": "raspi_2"})
    assert raspi_2.status_code == starlette.status.HTTP_200_OK

    user_1 = await async_client.post(
        "/v2/users/", json={"raspi_id": raspi_1.json()["id"], "name": "user_1"}
    )
    assert user_1.status_code == starlette.status.HTTP_200_OK
    user_2 = await async_client.post(
        "/v2/users/", json={"raspi_id": raspi_2.json()["id"], "name": "user_2"}
    )
    assert user_2.status_code == starlette.status.HTTP_200_OK

    couple_1 = await async_client.post(
        "/v2/couples/",
        json={
            "user1_id": user_1.json()["id"],
            "user2_id": user_2.json()["id"],
            "name": "couple_1",
        },
    )
    assert couple_1.status_code == starlette.status.HTTP_200_OK

    return {
        "raspi_1": raspi_1.json(),
        "raspi_2": raspi_2.json(),
        "user_1": user_1.json(),
        "user_2": user_2.json(),
        "couple_1": couple_1.json(),
    }
