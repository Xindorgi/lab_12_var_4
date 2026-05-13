from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, auth, database
from ..crud import vacancies as crud

router = APIRouter(prefix="/vacancies", tags=["vacancies"])

@router.post("/", response_model=schemas.VacancyOut)
def create_vacancy(
    vacancy: schemas.VacancyCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("employer", "admin"))
):
    return crud.create_vacancy(db, vacancy, current_user.id)

@router.get("/", response_model=list[schemas.VacancyOut])
def read_vacancies(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(database.get_db)
):
    return crud.get_vacancies(db, skip, limit, active_only)

@router.get("/{vacancy_id}", response_model=schemas.VacancyOut)
def read_vacancy(
    vacancy_id: int,
    db: Session = Depends(database.get_db)
):
    vac = crud.get_vacancy(db, vacancy_id)
    if not vac:
        raise HTTPException(status_code=404, detail="Not found")
    return vac

@router.put("/{vacancy_id}", response_model=schemas.VacancyOut)
def update_vacancy(
    vacancy_id: int, vacancy: schemas.VacancyCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("employer", "admin"))
):
    result = crud.update_vacancy(db, vacancy_id, vacancy, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Not your vacancy")
    return result

@router.delete("/{vacancy_id}")
def delete_vacancy(
    vacancy_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("employer", "admin"))
):
    result = crud.delete_vacancy(db, vacancy_id, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Not found")
    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Not your vacancy")
    return {"ok": True}