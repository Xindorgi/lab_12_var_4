from .conftest import create_user, auth_header
from app.models import Vacancy, Application

def test_schedule_interview(client, db):
    emp = create_user(db, "e@i.com", "employer")
    cand = create_user(db, "c@i.com", "candidate")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    headers_cand = auth_header(cand.id)
    app_resp = client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers_cand)
    app_id = app_resp.json()["id"]
    headers_emp = auth_header(emp.id)
    resp = client.post("/interviews/", json={
        "application_id": app_id,
        "scheduled_time": "2025-06-01T10:00:00",
        "location": "Office"
    }, headers=headers_emp)
    assert resp.status_code == 200
    assert resp.json()["location"] == "Office"

def test_schedule_interview_as_candidate_forbidden(client, db):
    cand = create_user(db, "c2@i.com", "candidate")
    emp = create_user(db, "e2@i.com", "employer")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    headers_cand = auth_header(cand.id)
    app_resp = client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers_cand)
    app_id = app_resp.json()["id"]
    resp = client.post("/interviews/", json={
        "application_id": app_id,
        "scheduled_time": "2025-06-01T10:00:00"
    }, headers=headers_cand)
    assert resp.status_code == 403

def test_get_interviews_by_application(client, db):
    emp = create_user(db, "e3@i.com", "employer")
    cand = create_user(db, "c3@i.com", "candidate")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    headers_cand = auth_header(cand.id)
    app_resp = client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers_cand)
    app_id = app_resp.json()["id"]
    headers_emp = auth_header(emp.id)
    client.post("/interviews/", json={
        "application_id": app_id,
        "scheduled_time": "2025-06-01T10:00:00"
    }, headers=headers_emp)
    resp = client.get(f"/interviews/by-application/{app_id}", headers=headers_cand)
    assert resp.status_code == 200
    assert len(resp.json()) == 1