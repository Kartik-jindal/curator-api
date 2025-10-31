# tests/test_users.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# --- Test Database Setup ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Dependency Override ---
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

# --- Test Client Setup ---
client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    """
    A pytest fixture that creates and tears down the database tables for each test.
    This ensures that each test function runs with a clean, isolated database.
    """
    # Setup: Create all tables before the test runs.
    Base.metadata.create_all(bind=engine)
    try:
        # Yield control to the test function.
        yield
    finally:
        # Teardown: Drop all tables after the test finishes.
        Base.metadata.drop_all(bind=engine)


def test_read_root():
    """
    Tests that the root endpoint ("/") returns a successful response and the expected message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Curator API!"}

def test_create_user_success(test_db):
    """
    Tests successful user creation via the POST /users/ endpoint.
    The `test_db` argument tells pytest to use the fixture we defined above.
    """
    # 1. Define the data for the new user.
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User"
    }

    # 2. Make the POST request using the TestClient.
    response = client.post("/users/", json=user_data)

    # 3. Assert the HTTP status code is 200 OK.
    assert response.status_code == 200, response.text
    
    # 4. Parse the JSON response body.
    data = response.json()

    # 5. Assert the response body contains the correct data.
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "created_at" in data
    
    # 6. CRITICAL: Assert that the hashed password is NOT exposed in the response.
    assert "hashed_password" not in data


def test_create_user_duplicate_email(test_db):
    """
    Tests that the API returns a 400 error when trying to create a user
    with an email that already exists.
    """
    # 1. Define the user data.
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "full_name": "Test User"
    }

    # 2. Act Part 1: Create the first user. We expect this to succeed.
    response1 = client.post("/users/", json=user_data)
    assert response1.status_code == 200, "First user creation failed when it should have succeeded."

    # 3. Act Part 2: Try to create a user with the exact same email again.
    response2 = client.post("/users/", json=user_data)

    # 4. Assert the failure case.
    assert response2.status_code == 400, "API did not return 400 on duplicate email."
    
    # 5. Assert the error message is correct.
    data = response2.json()
    assert data["detail"] == "Email already registered"