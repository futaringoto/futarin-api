import pytest
import starlette.status


@pytest.mark.asyncio
async def test_crud_raspi_no_name(async_client):
    # 新規作成：名前なしで作成
    res_1 = await async_client.post("/v2/raspis/", json={})
    assert res_1.status_code == starlette.status.HTTP_200_OK
    res_post = res_1.json()
    raspi_id = res_post["id"]

    # 一覧表示：ラズパイが一つだけ登録されているか確認
    res_2 = await async_client.get("/v2/raspis/")
    assert res_2.status_code == starlette.status.HTTP_200_OK
    res_get = res_2.json()
    assert isinstance(res_get, list)
    assert len(res_get) == 1

    # 更新：ラズパイの名前を変更
    res_3 = await async_client.put(f"/v2/raspis/{raspi_id}", json={"name": "hoge"})
    assert res_3.status_code == starlette.status.HTTP_200_OK
    res_put = res_3.json()
    assert res_put["name"] == "hoge"

    # 削除：ラズパイを消去
    res_4 = await async_client.delete(f"/v2/raspis/{raspi_id}")
    assert res_4.status_code == starlette.status.HTTP_200_OK

    # 削除後のラズパイが残っていないことを確認
    res_5 = await async_client.delete(f"/v2/raspis/{raspi_id}")
    assert res_5.status_code == starlette.status.HTTP_404_NOT_FOUND
