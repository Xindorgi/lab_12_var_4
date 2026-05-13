from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import database, auth
from ..models import Vacancy, Application

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/vacancies-stats")
def vacancies_stats(db: Session = Depends(database.get_db),
                    current_user = Depends(auth.require_role("admin"))):
    total = db.query(func.count(Vacancy.id)).scalar()
    active = db.query(func.count(Vacancy.id)).filter(Vacancy.is_active == True).scalar()
    return {"total": total, "active": active}

@router.get("/applications-by-vacancy")
def apps_by_vacancy(db: Session = Depends(database.get_db),
                    current_user = Depends(auth.require_role("admin", "employer"))):
    result = db.query(
        Vacancy.title,
        func.count(Application.id).label("count")
    ).join(Application, Vacancy.id == Application.vacancy_id, isouter=True) \
     .group_by(Vacancy.id).all()
    return [{"vacancy": r.title, "applications": r.count} for r in result]