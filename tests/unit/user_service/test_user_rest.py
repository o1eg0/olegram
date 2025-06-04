import uuid, pytest


def test_register_user(test_client):
    resp = test_client.post("/users/register", json=dict(username="bob", password="123"))
    assert resp.status_code == 201


def test_duplicate_username(test_client):
    test_client.post("/users/register", json=dict(username="bob", password="123"))
    resp = test_client.post("/users/register", json=dict(username="bob", password="xxx"))
    assert resp.status_code == 400


def test_login_returns_jwt(test_client):
    test_client.post("/users/register", json=dict(username="bob", password="123"))
    resp = test_client.post("/users/login", data=dict(username="bob", password="123"))
    assert "jwt-token" in resp.cookies
