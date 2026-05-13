from .conftest import create_user, auth_header
from app.models import Vacancy

def test_vacancies_stats_as_admin(client, db):
    admin = create_user(db, "admin@t.com", "admin")
    headers = auth_header(admin.id)
    vac1 = Vacancy(title="A", salary_min=0, employer_id=admin.id, is_active=True)
    vac2 = Vacancy(title="B", salary_min=0, employer_id=admin.id, is_active=False)
    db.add_all([vac1, vac2])
    db.commit()
    resp = client.get("/analytics/vacancies-stats", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 2
    assert data["active"] == 1

def test_vacancies_stats_as_employer_forbidden(client, db):
    user = create_user(db, "emp@t.com", "employer")
    headers = auth_header(user.id)
    resp = client.get("/analytics/vacancies-stats", headers=headers)
    assert resp.status_code == 403

def test_applications_by_vacancy(client, db):
    admin = create_user(db, "adm2@t.com", "admin")
    emp = create_user(db, "e@t.com", "employer")
    cand = create_user(db, "c@t.com", "candidate")
    vac = Vacancy(title="Dev", salary_min=0, employer_id=emp.id, is_active=True)
    db.add(vac)
    db.commit()
    db.refresh(vac)

    # кандидат подаёт заявку
    from app.models import Application
    app = Application(candidate_id=cand.id, vacancy_id=vac.id, status="applied")
    db.add(app)
    db.commit()

    headers = auth_header(admin.id)
    resp = client.get("/analytics/applications-by-vacancy", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["vacancy"] == "Dev"
    assert data[0]["applications"] == 1