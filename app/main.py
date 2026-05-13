from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routers import auth, vacancies, resumes, applications, interviews, analytics, frontend

Base.metadata.create_all(bind=engine)

app = FastAPI(title="HR Platform")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(vacancies.router)
app.include_router(resumes.router)
app.include_router(applications.router)
app.include_router(interviews.router)
app.include_router(analytics.router)

app.include_router(frontend.router)