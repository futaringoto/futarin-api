import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_transcribe_and_respond(client: TestClient):
    audio_file_path = "tests/audio1.wav"
    with open(audio_file_path, "rb") as audio_file:
        files = {"file": ("audio1.wav", audio_file, "multipart/form-data")}

        response = client.post("/v1/raspi", files=files)

    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mp3"
    assert response.content is not None
