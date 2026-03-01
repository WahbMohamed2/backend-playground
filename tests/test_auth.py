def test_register_success(client):
    response = client.post("/auth/register", json={
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    # Why this assert: hashed_password must never appear in response
    assert "password" not in data
    assert "hashed_password" not in data

def test_register_duplicate_email(client):
    # Register once
    client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "username": "dupuser1",
        "password": "password123"
    })
    # Try again with same email
    response = client.post("/auth/register", json={
        "email": "duplicate@example.com",
        "username": "dupuser2",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]

def test_login_success(client):
    client.post("/auth/register", json={
        "email": "logintest@example.com",
        "username": "logintest",
        "password": "password123"
    })
    response = client.post("/auth/login", json={
        "email": "logintest@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    response = client.post("/auth/login", json={
        "email": "logintest@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_get_me(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
