import pytest
from main import app


@pytest.fixture()
def client():
    return app.test_client()


def test_homepage_request(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'"status":"OK"' in response.data


def test_secret_request(client):
    response = client.get("/download/shared-config?key=secret-password")
    assert response.status_code == 200


def test_secret_bad_path(client):
    response = client.get("/download/shared-con?key=secret-password")
    assert response.status_code == 404


def test_secret_bad_key(client):
    response = client.get("/download/shared-config?key=secret-password2")
    assert response.status_code == 404


# DOWNLOAD_PATH = "shared-config"
# DOWNLOAD_KEY = "secret-password"
# PROTECTED_FILE = "tests/data/info.txt"
