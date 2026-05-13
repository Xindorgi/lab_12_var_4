from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, auth, database
from ..crud import resumes as crud

router = APIRouter(prefix="/resumes", tags=["resumes"])

@router.post("/", response_model=schemas.ResumeOut)
def create_resume(
    resume: schemas.ResumeCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("candidate", "admin"))
):
    if current_user.role != "candidate" and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only candidates can have a resume")
    return crud.create_or_update_resume(db, current_user.id, resume)

@router.get("/my", response_model=schemas.ResumeOut)
def get_my_resume(
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("candidate", "admin"))
):
    resume = crud.get_resume(db, current_user.id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@router.put("/my", response_model=schemas.ResumeOut)
def update_my_resume(
    resume: schemas.ResumeCreate,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("candidate", "admin"))
):
    return crud.create_or_update_resume(db, current_user.id, resume)

@router.delete("/my")
def delete_my_resume(
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.require_role("candidate", "admin"))
):
    if crud.delete_resume(db, current_user.id):
        return {"ok": True}
    raise HTTPException(status_code=404, detail="Resume not found")