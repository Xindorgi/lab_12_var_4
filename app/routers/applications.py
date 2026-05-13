from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, auth, database
from ..crud import applications as crud

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=schemas.ApplicationOut)
def apply(
    application: schemas.ApplicationCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("candidate", "admin"))
):
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can apply")
    result = crud.create_application(db, application, current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Vacancy not found or not active")
    return result

@router.get("/my", response_model=list[schemas.ApplicationOut])
def my_applications(
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("candidate", "admin"))
):
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can view their applications")
    return crud.get_applications_by_candidate(db, current_user.id)

@router.get("/to-me", response_model=list[schemas.ApplicationOut])
def applications_to_my_vacancies(
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("employer", "admin"))
):
    if current_user.role != "employer" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return crud.get_applications_for_employer(db, current_user.id)

@router.patch("/{application_id}/status", response_model=schemas.ApplicationOut)
def update_status(
    application_id: int,
    status_update: schemas.ApplicationUpdate,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("employer", "admin"))
):
    if not status_update.status:
        raise HTTPException(status_code=400, detail="Status is required")
    result = crud.update_application_status(
        db, application_id, status_update.status,
        current_user.id, current_user.role
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Application not found")
    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Not your vacancy")
    return result

@router.get("/all", response_model=list[schemas.ApplicationOut])
def get_all_applications(
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("admin"))
):
    return crud.get_all_applications(db)