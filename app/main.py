from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from .database import engine, Base
from .routers import auth, vacancies, resumes, applications, interviews, analytics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HR Platform")

app.include_router(auth.router)
app.include_router(vacancies.router)
app.include_router(resumes.router)
app.include_router(applications.router)
app.include_router(interviews.router)
app.include_router(analytics.router)