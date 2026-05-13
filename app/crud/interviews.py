from sqlalchemy.orm import Session
from .. import models, schemas

def create_interview(db: Session, interview: schemas.InterviewCreate, user_id: int, user_role: str):
    # проверить, что заявка существует и принадлежит вакансии работодателя (или админ)
    application = db.query(models.Application).filter(models.Application.id == interview.application_id).first()
    if not application:
        return None
    if user_role != "admin":
        vacancy = db.query(models.Vacancy).filter(models.Vacancy.id == application.vacancy_id).first()
        if not vacancy or vacancy.employer_id != user_id:
            return "forbidden"
    db_interview = models.Interview(**interview.model_dump())
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

def get_interviews_by_application(db: Session, application_id: int):
    return db.query(models.Interview).filter(models.Interview.application_id == application_id).all()