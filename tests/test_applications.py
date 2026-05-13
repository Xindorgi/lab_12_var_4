from .conftest import create_user, auth_header
from app.models import Vacancy, Application

def test_apply_to_active_vacancy(client, db):
    emp = create_user(db, "e@t.com", "employer")
    cand = create_user(db, "c@t.com", "candidate")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp.id, is_active=True)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    headers = auth_header(cand.id)
    resp = client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "applied"

def test_apply_to_inactive_vacancy(client, db):
    emp = create_user(db, "e2@t.com", "employer")
    cand = create_user(db, "c2@t.com", "candidate")
    vac = Vacancy(title="Old", salary_min=0, employer_id=emp.id, is_active=False)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    headers = auth_header(cand.id)
    resp = client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers)
    assert resp.status_code == 404  # наша реализация возвращает 404

def test_apply_as_employer_forbidden(client, db):
    emp = create_user(db, "e3@t.com", "employer")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp.id, is_active=True)
    db.add(vac)
    db.commit()
    headers = auth_header(emp.id)
    resp = client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers)
    assert resp.status_code == 403

def test_my_applications(client, db):
    cand = create_user(db, "c4@t.com", "candidate")
    emp = create_user(db, "e4@t.com", "employer")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    headers = auth_header(cand.id)
    # создадим отклик
    client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers)
    resp = client.get("/applications/my", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

def test_applications_to_my_vacancies(client, db):
    emp = create_user(db, "e5@t.com", "employer")
    cand = create_user(db, "c5@t.com", "candidate")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    # кандидат подаёт
    headers_cand = auth_header(cand.id)
    client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers_cand)
    # работодатель смотрит
    headers_emp = auth_header(emp.id)
    resp = client.get("/applications/to-me", headers=headers_emp)
    assert resp.status_code == 200
    assert len(resp.json()) == 1

def test_update_application_status(client, db):
    emp = create_user(db, "e6@t.com", "employer")
    cand = create_user(db, "c6@t.com", "candidate")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    headers_cand = auth_header(cand.id)
    app_resp = client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers_cand)
    app_id = app_resp.json()["id"]
    headers_emp = auth_header(emp.id)
    resp = client.patch(f"/applications/{app_id}/status", json={"status": "interviewed"}, headers=headers_emp)
    assert resp.status_code == 200
    assert resp.json()["status"] == "interviewed"

def test_update_status_another_employer_forbidden(client, db):
    emp1 = create_user(db, "e7@t.com", "employer")
    emp2 = create_user(db, "e8@t.com", "employer")
    cand = create_user(db, "c7@t.com", "candidate")
    vac = Vacancy(title="Job", salary_min=0, employer_id=emp1.id)
    db.add(vac)
    db.commit()
    db.refresh(vac)
    headers_cand = auth_header(cand.id)
    app_resp = client.post("/applications/", json={"vacancy_id": vac.id}, headers=headers_cand)
    app_id = app_resp.json()["id"]
    headers_emp2 = auth_header(emp2.id)
    resp = client.patch(f"/applications/{app_id}/status", json={"status": "rejected"}, headers=headers_emp2)
    assert resp.status_code == 403

def test_get_all_applications_as_admin(client, db):
    admin = create_user(db, "admin@test.com", "admin")
    emp = create_user(db, "emp@test.com", "employer")
    cand1 = create_user(db, "c1@test.com", "candidate")
    cand2 = create_user(db, "c2@test.com", "candidate")

    from app.models import Vacancy
    vac1 = Vacancy(title="Dev", salary_min=0, employer_id=emp.id, is_active=True)
    vac2 = Vacancy(title="QA", salary_min=0, employer_id=emp.id, is_active=True)
    db.add_all([vac1, vac2])
    db.commit()
    db.refresh(vac1)
    db.refresh(vac2)

    from app.models import Application
    app1 = Application(candidate_id=cand1.id, vacancy_id=vac1.id, status="applied")
    app2 = Application(candidate_id=cand2.id, vacancy_id=vac2.id, status="applied")
    db.add_all([app1, app2])
    db.commit()

    headers = auth_header(admin.id)
    resp = client.get("/applications/all", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2

def test_get_all_applications_as_employer_forbidden(client, db):
    emp = create_user(db, "emp@test.com", "employer")
    headers = auth_header(emp.id)
    resp = client.get("/applications/all", headers=headers)
    assert resp.status_code == 403