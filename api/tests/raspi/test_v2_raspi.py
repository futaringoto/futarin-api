import pytest
import starlette.status


@pytest.mark.asyncio
async def test_transcribe_and_respond(async_client, raspi_fixture):
    raspi_1 = raspi_fixture["raspi_1"]
    audio_file_path = "tests/audio1.wav"
    with open(audio_file_path, "rb") as audio_file:
        files = {"file": ("audio1.wav", audio_file, "multipart/form-data")}

        response = await async_client.post(
            f"/v2/raspis/{raspi_1["id"]}",
            files=files,
        )

    assert response.status_code == starlette.status.HTTP_200_OK
    assert response.headers["content-type"] == "audio/wav"
    assert response.content is not None


# @pytest.mark.asyncio
# async def test_send_message(async_client, raspi_fixture):
#    raspi_1 = raspi_fixture["raspi_1"]
#    audio_file_path = "tests/audio1.wav"
#    with open(audio_file_path, "rb") as audio_file:
#        files = {"file": ("audio1.wav", audio_file, "multipart/form-data")}
#
#        response = await async_client.post(
#            f"/v2/raspis/{raspi_1["id"]}/messages",
#            files=files,
#        )
#
#    assert response.status_code == starlette.status.HTTP_200_OK
