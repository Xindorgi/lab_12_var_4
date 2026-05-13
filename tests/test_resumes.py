from .conftest import create_user, auth_header

def test_create_resume_as_candidate(client, db):
    user = create_user(db, "cand@test.com", "candidate")
    headers = auth_header(user.id)
    resp = client.post("/resumes/", json={
        "full_name": "John Doe", "phone": "12345", "skills": "Python"
    }, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "John Doe"

def test_create_resume_as_employer_forbidden(client, db):
    user = create_user(db, "emp@test.com", "employer")
    headers = auth_header(user.id)
    resp = client.post("/resumes/", json={"full_name": "Test"}, headers=headers)
    assert resp.status_code == 403

def test_get_my_resume(client, db):
    user = create_user(db, "cand2@test.com", "candidate")
    headers = auth_header(user.id)
    # сначала создадим
    client.post("/resumes/", json={"full_name": "Alice"}, headers=headers)
    resp = client.get("/resumes/my", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Alice"

def test_update_resume(client, db):
    user = create_user(db, "cand3@test.com", "candidate")
    headers = auth_header(user.id)
    client.post("/resumes/", json={"full_name": "Bob"}, headers=headers)
    resp = client.put("/resumes/my", json={"full_name": "Bobby"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["full_name"] == "Bobby"

def test_delete_resume(client, db):
    user = create_user(db, "cand4@test.com", "candidate")
    headers = auth_header(user.id)
    client.post("/resumes/", json={"full_name": "Del"}, headers=headers)
    resp = client.delete("/resumes/my", headers=headers)
    assert resp.status_code == 200
    # проверяем, что удалилось
    resp2 = client.get("/resumes/my", headers=headers)
    assert resp2.status_code == 404