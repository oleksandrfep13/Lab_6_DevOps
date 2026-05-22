import os
import pytest

os.environ["POSTGRES_USER"] = "postgres"
os.environ["POSTGRES_PASSWORD"] = "postgres"
os.environ["POSTGRES_HOST"] = "db"
os.environ["POSTGRES_DB"] = "devops_lab"

from app.app import create_app


@pytest.fixture
def client():
    app = create_app()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")

    assert response.status_code == 200


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={"title": "Test task"}
    )

    assert response.status_code == 201