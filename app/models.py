from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="candidate")  # admin, employer, candidate
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="user", uselist=False, cascade="all, delete-orphan")
    vacancies = relationship("Vacancy", back_populates="employer")
    applications = relationship("Application", back_populates="candidate", foreign_keys="Application.candidate_id")

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String)
    skills = Column(Text)
    experience = Column(Text)
    education = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="resume")

class Vacancy(Base):
    __tablename__ = "vacancies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    requirements = Column(Text)
    salary_min = Column(Float, default=0)
    salary_max = Column(Float, default=0)
    employer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    employer = relationship("User", back_populates="vacancies")
    applications = relationship("Application", back_populates="vacancy")

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vacancy_id = Column(Integer, ForeignKey("vacancies.id"), nullable=False)
    status = Column(String, default="applied")
    cover_letter = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    candidate = relationship("User", back_populates="applications", foreign_keys=[candidate_id])
    vacancy = relationship("Vacancy", back_populates="applications")
    interviews = relationship("Interview", back_populates="application", cascade="all, delete-orphan")

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    scheduled_time = Column(DateTime, nullable=False)
    location = Column(String)
    notes = Column(Text)
    status = Column(String, default="scheduled")
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="interviews")