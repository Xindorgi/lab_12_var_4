from .conftest import create_user

def test_register(client):
    resp = client.post("/auth/register", json={
        "email": "new@test.com", "password": "123456", "role": "candidate"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["email"] == "new@test.com"
    assert data["role"] == "candidate"

def test_register_duplicate(client, db):
    create_user(db, "dup@test.com", "candidate")
    resp = client.post("/auth/register", json={
        "email": "dup@test.com", "password": "123456", "role": "candidate"
    })
    assert resp.status_code == 400
    assert "already registered" in resp.json()["detail"].lower()

def test_login(client, db):
    create_user(db, "login@test.com", "employer", "mypass")
    resp = client.post("/auth/login", data={
        "username": "login@test.com", "password": "mypass"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, db):
    create_user(db, "wrong@test.com", "candidate", "correct")
    resp = client.post("/auth/login", data={
        "username": "wrong@test.com", "password": "incorrect"
    })
    assert resp.status_code == 401

def test_access_protected_without_token(client):
    resp = client.get("/vacancies/")
    assert resp.status_code == 200

def test_access_with_invalid_token(client):
    resp = client.get("/vacancies/", headers={"Authorization": "Bearer fake.token.here"})
    assert resp.status_code == 200

def test_create_vacancy_without_token(client):
    resp = client.post("/vacancies/", json={"title": "Test"})
    assert resp.status_code == 401

def test_create_vacancy_with_invalid_token(client):
    resp = client.post("/vacancies/", json={"title": "Test"}, headers={"Authorization": "Bearer fake.token.here"})
    assert resp.status_code == 401