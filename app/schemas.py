from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "candidate"

class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class ResumeCreate(BaseModel):
    full_name: str
    phone: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None

class ResumeOut(ResumeCreate):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config: from_attributes = True

class VacancyCreate(BaseModel):
    title: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_min: Optional[float] = 0
    salary_max: Optional[float] = 0
    is_active: Optional[bool] = True

class VacancyOut(VacancyCreate):
    id: int
    employer_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config: from_attributes = True

class ApplicationCreate(BaseModel):
    vacancy_id: int
    cover_letter: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    cover_letter: Optional[str] = None

class ApplicationOut(BaseModel):
    id: int
    candidate_id: int
    vacancy_id: int
    status: str
    cover_letter: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    class Config: from_attributes = True

class InterviewCreate(BaseModel):
    application_id: int
    scheduled_time: datetime
    location: Optional[str] = None
    notes: Optional[str] = None

class InterviewOut(InterviewCreate):
    id: int
    status: str
    created_at: datetime
    class Config: from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str