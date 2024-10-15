import pytest
import starlette.status


@pytest.fixture
async def create_raspi(async_client):
    response = await async_client.post("/v2/raspis/", json={})
    assert response.status_code == starlette.status.HTTP_200_OK
    return response.json()


@pytest.mark.asyncio
async def test_crud_user_no_name(async_client, create_raspi):
    raspi_id = create_raspi["id"]
    # 新規作成：名前なしで新規ユーザ作成
    res_1 = await async_client.post("/v2/users/", json={"raspi_id": raspi_id})
    assert res_1.status_code == starlette.status.HTTP_200_OK
    res_post = res_1.json()
    assert res_post["raspi_id"] == raspi_id
    user_id = res_post["id"]

    # 一覧表示：ユーザが一つだけ登録されているか確認
    res_2 = await async_client.get("/v2/users/")
    assert res_2.status_code == starlette.status.HTTP_200_OK
    res_get = res_2.json()
    assert isinstance(res_get, list)
    assert len(res_get) == 1

    # 更新：名前を変更
    res_3 = await async_client.put(
        f"/v2/users/{user_id}", json={"name": "hoge", "raspi_id": raspi_id}
    )
    assert res_3.status_code == starlette.status.HTTP_200_OK
    res_put = res_3.json()
    assert res_put["name"] == "hoge"

    # TODO:ラズパイを削除した時、raspi_idがnullになるか？
    # res_4 = await async_client.delete(f"/v2/raspis/{raspi_id}")
    # assert res_4.status_code == starlette.status.HTTP_200_OK
    # res_5 = await async_client.get("/v2/users/")
    # assert res_5.status_code == starlette.status.HTTP_200_OK
    # res_get_2 = res_5.json()
    # assert res_get_2[0]["raspi_id"] == None

    # TODO:登録されていないラズパイを紐付けようとした場合404を返す
    # res_5 = await async_client.put(
    #    f"/v2/users/{user_id}",
    #    json={"name": "hoge", "raspi_id": 2}
    # )
    # assert res_5.status_code == starlette.status.HTTP_404_NOT_FOUND

    # 削除：ユーザを消去
    res_6 = await async_client.delete(f"/v2/users/{user_id}")
    assert res_6.status_code == starlette.status.HTTP_200_OK

    # 削除後のユーザが残っていないことを確認
    res7 = await async_client.delete(f"/v2/users/{user_id}")
    assert res7.status_code == starlette.status.HTTP_404_NOT_FOUND
