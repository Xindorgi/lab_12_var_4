import pytest
from .conftest import create_user, auth_header
from app.models import Vacancy

def test_create_vacancy_employer(client, db):
    user = create_user(db, "boss@test.com", "employer")
    headers = auth_header(user.id)
    resp = client.post("/vacancies/", json={
        "title": "Developer", "salary_min": 1000, "salary_max": 5000
    }, headers=headers)
    print("STATUS:", resp.status_code)
    print("BODY:", resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Developer"
    assert data["employer_id"] == user.id

def test_create_vacancy_candidate_forbidden(client, db):
    user = create_user(db, "cand@test.com", "candidate")
    headers = auth_header(user.id)
    resp = client.post("/vacancies/", json={"title": "Hack"}, headers=headers)
    assert resp.status_code == 403

def test_get_vacancies_active_only(client, db):
    user = create_user(db, "emp@test.com", "employer")
    headers = auth_header(user.id)
    # две вакансии: активная и неактивная
    v1 = Vacancy(title="Active", salary_min=0, employer_id=user.id, is_active=True)
    v2 = Vacancy(title="Inactive", salary_min=0, employer_id=user.id, is_active=False)
    db.add_all([v1, v2])
    db.commit()
    resp = client.get("/vacancies/?active_only=true", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["title"] == "Active"

def test_get_vacancy_by_id(client, db):
    user = create_user(db, "emp2@test.com", "employer")
    headers = auth_header(user.id)
    vac = Vacancy(title="Some", salary_min=100, employer_id=user.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    resp = client.get(f"/vacancies/{vac.id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Some"

def test_update_own_vacancy(client, db):
    user = create_user(db, "owner@test.com", "employer")
    headers = auth_header(user.id)
    vac = Vacancy(title="Old", salary_min=10, employer_id=user.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    resp = client.put(f"/vacancies/{vac.id}", json={"title": "New"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "New"

def test_update_another_vacancy_forbidden(client, db):
    user1 = create_user(db, "u1@test.com", "employer")
    user2 = create_user(db, "u2@test.com", "employer")
    headers = auth_header(user1.id)
    vac = Vacancy(title="User2 Vac", salary_min=0, employer_id=user2.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    resp = client.put(f"/vacancies/{vac.id}", json={"title": "Stolen"}, headers=headers)
    assert resp.status_code == 403

def test_delete_own_vacancy(client, db):
    user = create_user(db, "del@test.com", "employer")
    headers = auth_header(user.id)
    vac = Vacancy(title="Delete me", salary_min=0, employer_id=user.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    resp = client.delete(f"/vacancies/{vac.id}", headers=headers)
    assert resp.status_code == 200
    assert db.query(Vacancy).filter(Vacancy.id == vac.id).first() is None

def test_delete_another_vacancy_forbidden(client, db):
    user1 = create_user(db, "x@test.com", "employer")
    user2 = create_user(db, "y@test.com", "employer")
    headers = auth_header(user1.id)
    vac = Vacancy(title="Y Vac", salary_min=0, employer_id=user2.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    resp = client.delete(f"/vacancies/{vac.id}", headers=headers)
    assert resp.status_code == 403

def test_empty_title_validation(client, db):
    user = create_user(db, "val@test.com", "employer")
    headers = auth_header(user.id)
    resp = client.post("/vacancies/", json={"title": ""}, headers=headers)
    assert resp.status_code == 422