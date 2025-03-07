import pytest


@pytest.mark.parametrize(
    "login, password, email",
    [
        ("unique_user", "some_password", "unique_user@example.com"),
        ("another_user", "qwerty123", "another@example.com"),
    ],
)
def test_register_user_success(client, login, password, email):
    payload = {"login": login, "password": password, "email": email}
    response = client.post("/register", json=payload)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["login"] == login
    assert data["email"] == email
    assert "id" in data


def test_register_user_already_exists(client):
    payload = {
        "login": "test_user",
        "password": "secret",
        "email": "test_user@example.com",
    }
    resp1 = client.post("/register", json=payload)
    assert resp1.status_code == 200

    resp2 = client.post("/register", json=payload)
    assert resp2.status_code == 400
    data = resp2.json()
    assert data["detail"] == "User with this username already exists"


def test_auth_user_success(client):
    payload_reg = {
        "login": "test_user_auth",
        "password": "secret_auth",
        "email": "auth@example.com",
    }
    resp = client.post("/register", json=payload_reg)
    assert resp.status_code == 200

    payload_auth = {"username": "test_user_auth", "password": "secret_auth"}
    response = client.post("/auth", json=payload_auth)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["status"] == "success"


def test_auth_user_invalid_credentials(client):
    payload_reg = {
        "login": "test_user_wrongpass",
        "password": "correct_pass",
        "email": "wrongpass@example.com",
    }
    resp = client.post("/register", json=payload_reg)
    assert resp.status_code == 200

    payload_auth = {"username": "test_user_wrongpass", "password": "invalid_password"}
    response = client.post("/auth", json=payload_auth)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid credentials"


def test_auth_user_not_found(client):
    payload_auth = {"username": "non_existent", "password": "secret"}
    response = client.post("/auth", json=payload_auth)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Invalid credentials"
