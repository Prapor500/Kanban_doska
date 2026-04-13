from tests.helpers import register_user


def test_register_login_and_duplicate_email(client):
    payload = {"email": "alice@example.com", "password": "secret123"}

    register_response = client.post("/auth/register", json=payload)
    assert register_response.status_code == 201
    register_body = register_response.json()
    assert register_body["status"] == "ok"
    assert isinstance(register_body["user_id"], int)

    login_response = client.post("/auth/login", json=payload)
    assert login_response.status_code == 200
    login_body = login_response.json()
    assert login_body["token_type"] == "Bearer"
    assert login_body["access_token"]

    duplicate_response = client.post("/auth/register", json=payload)
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Почта уже зарегистрирована"


def test_login_with_invalid_password_returns_401(client):
    register_user(client, "bob@example.com", "good-password")

    response = client.post(
        "/auth/login",
        json={"email": "bob@example.com", "password": "bad-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный email или пароль"
