from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, auth, database
from ..crud import interviews as crud

router = APIRouter(prefix="/interviews", tags=["interviews"])

@router.post("/", response_model=schemas.InterviewOut)
def schedule_interview(
    interview: schemas.InterviewCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("employer", "admin"))
):
    result = crud.create_interview(db, interview, current_user.id, current_user.role)
    if result is None:
        raise HTTPException(status_code=404, detail="Application not found")
    if result == "forbidden":
        raise HTTPException(status_code=403, detail="Not your vacancy")
    return result

@router.get("/by-application/{application_id}", response_model=list[schemas.InterviewOut])
def get_interviews(
    application_id: int,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.get_current_user)
):
    # доступно всем авторизованным, но можно добавить проверку роли
    return crud.get_interviews_by_application(db, application_id)