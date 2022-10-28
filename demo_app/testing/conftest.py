import json
import pytest
from fastapi.testclient import TestClient
from demo_app.main import app
from demo_app.database import Base, get_db


from domain import db
from domain.db import DBSession, engine

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    def override_get_db():
        try:
            db = DBSession()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client


@pytest.fixture
def token_header(client: TestClient):
    data = {
        "username": 'TestUser',
        "email": 'testuser1@user1.in',
        "password": 'TestUser@1234',
        "confirm_password": 'TestUser@1234'
    }
    response = client.post('/register', json.dumps(data))
    data = {
        "username": "testuser1@user1.in",
        "password": "TestUser@1234"
    }
    response = client.post("/login", json.dumps(data))
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print(response.json())
    print('++++++++++++++++++++++++++++++++++++++++++++')
    access_token = response.json()["access_token"]
    return f"Bearer {access_token}"
