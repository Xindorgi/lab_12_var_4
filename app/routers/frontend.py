from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader

router = APIRouter(include_in_schema=False)

env = Environment(loader=FileSystemLoader("templates"), auto_reload=True)

def render(name: str, request: Request, **kwargs):
    template = env.get_template(name)
    return HTMLResponse(template.render(request=request, **kwargs))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return render("vacancies.html", request)

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return render("login.html", request)

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return render("register.html", request)

@router.get("/vacancies", response_class=HTMLResponse)
async def vacancies_page(request: Request):
    return render("vacancies.html", request)

@router.get("/resume", response_class=HTMLResponse)
async def resume_page(request: Request):
    return render("my_resume.html", request)

@router.get("/applications", response_class=HTMLResponse)
async def applications_page(request: Request):
    return render("my_applications.html", request)

@router.get("/employer", response_class=HTMLResponse)
async def employer_page(request: Request):
    return render("my_vacancies.html", request)

@router.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    return render("admin.html", request)