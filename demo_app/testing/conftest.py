import json
import os

import pytest
from fastapi.testclient import TestClient
from demo_app.main import app
print('1.')
from domain.db import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from domain.db import init_db


SQLALCHEMY_DATABASE_URL = os.environ.get('TESTING_DATABASE_URL')
print(SQLALCHEMY_DATABASE_URL, '........')
engine = create_engine(SQLALCHEMY_DATABASE_URL)
print(engine, '>>>>>>')
TestingLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print(TestingLocal, '<<<<<<<<')
Session = TestingLocal

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    def override_get_db():
        # try:
        db = TestingLocal()
        yield db
        # finally:
        db.close()
    app.dependency_overrides[init_db] = override_get_db
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
    print('in Register')
    data = {
        "username": "testuser1@user1.in",
        "password": "TestUser@1234"
    }
    response = client.post("/login", json.dumps(data))
    print('in Login')
    print('++++++++++++++++++++++++++++++++++++++++++++')
    print(response.json())
    print('++++++++++++++++++++++++++++++++++++++++++++')
    access_token = response.json()["access_token"]
    return f"Bearer {access_token}"
