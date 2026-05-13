from sqlalchemy.orm import Session
from .. import models, schemas

def create_application(db: Session, application: schemas.ApplicationCreate, candidate_id: int):
    # проверка, что вакансия активна
    vacancy = db.query(models.Vacancy).filter(
        models.Vacancy.id == application.vacancy_id,
        models.Vacancy.is_active == True
    ).first()
    if not vacancy:
        return None
    db_app = models.Application(**application.model_dump(), candidate_id=candidate_id)
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

def get_applications_by_candidate(db: Session, candidate_id: int):
    return db.query(models.Application).filter(models.Application.candidate_id == candidate_id).all()

def get_applications_for_employer(db: Session, employer_id: int):
    # заявки на вакансии этого работодателя
    return db.query(models.Application).join(models.Vacancy).filter(
        models.Vacancy.employer_id == employer_id
    ).all()

def update_application_status(db: Session, application_id: int, status: str, user_id: int, user_role: str):
    app = db.query(models.Application).filter(models.Application.id == application_id).first()
    if not app:
        return None
    if user_role != "admin":
        vacancy = db.query(models.Vacancy).filter(models.Vacancy.id == app.vacancy_id).first()
        if not vacancy or vacancy.employer_id != user_id:
            return "forbidden"
    app.status = status
    db.commit()
    db.refresh(app)
    return app