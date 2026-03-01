import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.dependencies import get_db

# Why a separate test DB: tests should never touch real data
TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Why this fixture: creates all tables before tests, drops them after
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Why override get_db: swap the real DB session for the test one
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Why scope="module": one client shared across all tests in a file
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# Why this fixture: many tests need an auth token — create user once and reuse
@pytest.fixture(scope="module")
def auth_token(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123"
    })
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "testpass123"
    })
    return response.json()["access_token"]

# Why this fixture: returns headers dict so tests don't repeat this every time
@pytest.fixture(scope="module")
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}
