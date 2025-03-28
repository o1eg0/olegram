def test_get_profile_success(client):
    payload = {
        "login": "test_user",
        "password": "secret",
        "email": "test_user@example.com",
    }
    resp = client.post("/register", json=payload)
    assert resp.status_code == 200

    r = client.post("/test_user/profile")
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "test_user@example.com"


def test_get_profile_not_found(client):
    r = client.post("/user_does_not_exist/profile")
    assert r.status_code == 404
    data = r.json()
    assert data["detail"] == "User not found"


def test_update_profile_success(client):
    payload_reg = {
        "login": "profile_user",
        "password": "1234",
        "email": "profile@example.com",
    }
    resp = client.post("/register", json=payload_reg)
    assert resp.status_code == 200

    update_payload = {
        "email": "updated@example.com",
        "first_name": "UpdatedFirst",
        "bio": "UpdatedBio",
    }
    r = client.put("/profile_user/profile", json=update_payload)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "updated@example.com"
    assert data["first_name"] == "UpdatedFirst"
    assert data["bio"] == "UpdatedBio"


def test_update_profile_not_found(client):
    payload = {"email": "some@example.com"}
    response = client.put("/unknown_user/profile", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"
