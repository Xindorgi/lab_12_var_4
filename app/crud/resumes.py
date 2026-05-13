from sqlalchemy.orm import Session
from .. import models, schemas

def get_resume(db: Session, user_id: int):
    return db.query(models.Resume).filter(models.Resume.user_id == user_id).first()

def create_or_update_resume(db: Session, user_id: int, resume: schemas.ResumeCreate):
    db_resume = get_resume(db, user_id)
    if db_resume:
        for field, value in resume.model_dump(exclude_unset=True).items():
            setattr(db_resume, field, value)
    else:
        db_resume = models.Resume(**resume.model_dump(), user_id=user_id)
        db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume

def delete_resume(db: Session, user_id: int):
    db_resume = get_resume(db, user_id)
    if db_resume:
        db.delete(db_resume)
        db.commit()
        return True
    return False