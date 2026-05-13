from sqlalchemy.orm import Session
from .. import models, schemas

def get_vacancy(db: Session, vacancy_id: int):
    return db.query(models.Vacancy).filter(models.Vacancy.id == vacancy_id).first()

def get_vacancies(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False):
    q = db.query(models.Vacancy)
    if active_only:
        q = q.filter(models.Vacancy.is_active == True)
    return q.offset(skip).limit(limit).all()

def create_vacancy(db: Session, vacancy: schemas.VacancyCreate, employer_id: int):
    db_vacancy = models.Vacancy(**vacancy.model_dump(), employer_id=employer_id)
    db.add(db_vacancy)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

def update_vacancy(db: Session, vacancy_id: int, vacancy: schemas.VacancyCreate, user_id: int):
    db_vacancy = get_vacancy(db, vacancy_id)
    if not db_vacancy:
        return None
    if db_vacancy.employer_id != user_id:
        return "forbidden"
    for field, value in vacancy.model_dump(exclude_unset=True).items():
        setattr(db_vacancy, field, value)
    db.commit()
    db.refresh(db_vacancy)
    return db_vacancy

def delete_vacancy(db: Session, vacancy_id: int, user_id: int):
    db_vacancy = get_vacancy(db, vacancy_id)
    if not db_vacancy:
        return None
    if db_vacancy.employer_id != user_id:
        return "forbidden"
    db.delete(db_vacancy)
    db.commit()
    return True