# Лабораторная работа 12 — Вариант 4 — Ведешкин Андрей Георгиевич — группа 221131


## Общая структура проекта

```text
./
├── .github/
│   └── workflows/
│       └── pr-ai-review.yml
├── app/
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── applications.py
│   │   ├── interviews.py
│   │   ├── resumes.py
│   │   └── vacancies.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── applications.py
│   │   ├── auth.py
│   │   ├── frontend.py
│   │   ├── interviews.py
│   │   ├── resumes.py
│   │   └── vacancies.py
│   ├── __init__.py
│   ├── auth.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── static/
│   └── style.css
├── templates/
│   ├── admin.html
│   ├── base.html
│   ├── login.html
│   ├── my_applications.html
│   ├── my_resume.html
│   ├── my_vacancies.html
│   ├── register.html
│   └── vacancies.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_analytics.py
│   ├── test_applications.py
│   ├── test_auth.py
│   ├── test_interviews.py
│   ├── test_resumes.py
│   └── test_vacancies.py
├── .env.example
├── .gitignore
└── requirements.txt
```

---

## Реализованные задания повышенной сложности:

Создание полноценного веб-приложения;

Code review сгенерированного кода;

Интеграция ИИ в CI/CD;

Генерация unit-тестов с высоким покрытием;


---

## Взаимодействие с проектом

Ниже представлены команды для взаимодействия с проектом:
```
# Установка требуемых компонентов
pip install -r .\requirements.txt

# Поднятие сервера
uvicorn app.main:app --reload   

# Основная страница
http://127.0.0.1:8000/

# Запуск тестов
pytest --cov=app --cov-report=term-missing
```

## Тесты:
Тесты покрывают полностью логику проекта.

Проходят все 37/37 тестов.
