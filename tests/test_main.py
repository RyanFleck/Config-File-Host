import pytest
from main import app


@pytest.fixture()
def client():
    return app.test_client()


def test_request_example(client):
    response = client.get("/")
    assert b'"status":"OK"' in response.data
