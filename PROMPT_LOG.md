# 📋 Prompt Log  
*Документация процесса разработки с использованием AI-ассистента*

---

## 🧱 Коммит 1 — Модели данных и база

### Промпт 1

**Инструмент:** Deepseek

**Промпт:**
> Создай SQLAlchemy модели для HR-приложения:  
> - `User` (id, email, hashed_password, role = "applicant" | "recruiter" | "admin")  
> - `Vacancy` (id, title, description, company, created_by_id, created_at)  
> - `Resume` (id, title, skills, experience, user_id, created_at)  
> - `Application` (id, vacancy_id, resume_id, status = "pending" | "accepted" | "rejected", applied_at)  
> - `Interview` (id, application_id, scheduled_at, feedback)  
> Используй `declarative_base`, связи через `relationship`, типы колонок из `sqlalchemy`.  
> Код в `app/models.py`, без лишних комментариев. Напиши скрипт `init_db.py` для создания таблиц.

**Результат:**  
Получен `models.py` со всеми моделями, правильными внешними ключами и каскадным удалением.  
Добавлен `init_db.py`, который использует `create_all`. Проверка: таблицы создаются, связи корректны.

### Промпт 2

**Инструмент:** Deepseek 

**Промпт:**
> Добавь в `app/database.py` асинхронный движок `asyncpg`, фабрику сессий `async_sessionmaker`.  
> Нужна зависимость `get_db` для FastAPI — через `yield` сессию с автокоммитом/роллбэком.  
> Плюс утилита `get_sync_db` для скриптов и тестов (синхронная версия на `psycopg` или `sqlite` для тестов).  
> В `app/config.py` — чтение `DATABASE_URL` из `.env`. Используй `pydantic-settings`.

**Результат:**  
Асинхронная конфигурация БД, `get_db` с корректным закрытием, `get_sync_db` для миграций.  
Конфиг: `Settings` с `DATABASE_URL`, `APP_NAME`. Добавлен `.env.example`.

---

## 🔐 Коммит 2 — Аутентификация и роли

### Промпт 3

**Инструмент:** Deepseek 

**Промпт:**
> Реализуй авторизацию в `app/routers/auth.py`:  
> - POST `/register` — принимает email, password, role, хеширует через `bcrypt`, создаёт пользователя.  
> - POST `/login` — возвращает JWT access token (используй `python-jose`), время жизни 30 минут.  
> - GET `/users/me` — возвращает текущего пользователя (защищённый эндпоинт).  
> Напиши зависимость `get_current_user`, которая извлекает токен из заголовка `Authorization: Bearer ...` и поднимает `User` из БД.  
> Все схемы Pydantic вынеси в `app/schemas.py`.

**Результат:**  
`auth.py` с маршрутами, `get_current_user` кидает 401 при ошибке.  
Схемы: `UserCreate`, `UserOut`, `Token`.  
Тесты: `test_auth.py` проверяют регистрацию, логин, защищённый эндпоинт.

---

## 📄 Коммит 3 — CRUD вакансий и резюме

### Промпт 4

**Инструмент:** Deepseek

**Промпт:**
> Напиши CRUD для вакансий в `app/routers/vacancies.py`:  
> - GET `/vacancies` — список всех (пагинация: `skip`, `limit`).  
> - POST `/vacancies` — создание, доступно только для `recruiter` и `admin`.  
> - PUT `/vacancies/{id}` — обновление, владелец или admin.  
> - DELETE `/vacancies/{id}` — удаление, владелец или admin.  
> Используй зависимости проверки ролей (`get_current_user` + проверка `user.role`).  
> Все ответы — Pydantic схемы. Обрабатывай 404, 403.  
> Аналогичный CRUD для резюме (`app/routers/resumes.py`) — резюме может создавать и редактировать только его владелец (applicant).

**Результат:**  
Роутеры с валидацией прав, пагинацией, корректными статус-кодами.  
Схемы `VacancyCreate`, `VacancyOut`, `ResumeCreate`, `ResumeOut`.  
Тесты в `test_vacancies.py` и `test_resumes.py` покрывают позитивные и негативные сценарии.

---

## 🤝 Коммит 4 — Отклики на вакансии

### Промпт 5

**Инструмент:** Deepseek

**Промпт:**
> Добавь эндпоинты для откликов в `app/routers/applications.py`:  
> - POST `/applications` — applicant откликается на вакансию (нужно `vacancy_id` и своё `resume_id`).  
> - GET `/applications/my` — список откликов текущего пользователя.  
> - GET `/applications/for-my-vacancies` — для рекрутера: все отклики на его вакансии.  
> - PUT `/applications/{id}/status` — recruiter или admin меняют статус (`pending` → `accepted/rejected`).  
> Проверки: нельзя откликнуться повторно, нельзя откликнуться на свою вакансию, резюме должно принадлежать пользователю.  
> Все изменения должны сохраняться в БД, возвращать обновлённый объект.

**Результат:**  
Полноценный роутер с бизнес-логикой. Схемы `ApplicationCreate`, `ApplicationOut`, `ApplicationUpdate`.  
Тесты: проверяют дубликаты, права доступа, смену статуса.

---

## 📊 Коммит 5 — Аналитика

### Промпт 6

**Инструмент:** Deepseek

**Промпт:**
> В `app/routers/analytics.py` создай эндпоинт `GET /analytics/vacancy/{vacancy_id}` (доступен создателю вакансии и admin).  
> Он должен возвращать:  
> - общее количество откликов  
> - количество по статусам (pending/accepted/rejected)  
> - среднее время отклика (разница между `applied_at` и `created_at` вакансии)  
> Используй SQLAlchemy `func.count`, `case`, `func.avg`, `func.julianday` для SQLite или `EXTRACT` для PostgreSQL.  
> Для простоты сделай совместимым с SQLite (тестовая БД).  
> Напиши тест с замоканными данными.

**Результат:**  
Эндпоинт возвращает JSON со статистикой. В тестах — фабрика откликов с разными датами.  
Ошибка 403, если пользователь не владелец вакансии и не admin.

---

## 🎨 Коммит 6 — Шаблоны (фронтенд)

### Промпт 7

**Инструмент:** Deepseek  

**Промпт:**
> В `app/routers/frontend.py` сделай несколько HTML-страниц с использованием Jinja2:  
> - `/` — список вакансий (шаблон `vacancies.html`)  
> - `/my-resume` — форма создания/редактирования резюме (`my_resume.html`)  
> - `/my-applications` — список откликов текущего пользователя (`my_applications.html`)  
> - `/login`, `/register` — формы (`login.html`, `register.html`)  
> Используй `templates/` и `static/style.css` для стилей.  
> Подключи CSS — тёмная тема, карточки, адаптивная сетка.  
> В шаблонах должна быть навигация в зависимости от роли (через глобальную переменную `current_user`).  
> Все страницы рендерятся серверно, после успешных действий — редирект.

**Результат:**  
Роутер с `Jinja2Templates`. Зависимость `get_current_user_optional` для страниц.  
Формы отправляют данные на API (через `fetch` или стандартные POST).  
Результат — полноценный фронтенд без отдельного клиента.

---

## ⚙️ Коммит 7 — CI/CD: GitHub Actions для автоматического ревью PR

### Промпт 8

**Инструмент:** Deepseek

**Промпт:**
> Создай GitHub Actions workflow для автоматического анализа Pull Request с помощью LLM (например, через API llm7.io).  
> Требования:  
> - Триггер: `pull_request: [opened, synchronize]`  
> - Шаги: checkout кода, получение diff между base и HEAD, установка Python, генерация AI-ревью (суммаризация изменений, оценка рисков), публикация комментария в PR.  
> Используй переменную окружения `LLM7_API_KEY` из секретов GitHub.  
> Формат вывода: на русском, в стиле техлида.  
> Работоспособность должна быть проверена на тестовом PR.  
> Код workflow сохрани в `.github/workflows/pr-ai-review.yml`.

**Результат:**  
Создан файл `pr-ai-review.yml`. Workflow:  
- получает diff через `git diff origin/${{ github.base_ref }}...HEAD`  
- генерирует промпт с ограничением 12000 символов  
- вызывает `gpt-4o-mini` через OpenAI-совместимый клиент (base_url `https://api.llm7.io/v1`)  
- комментарий публикуется с помощью `thollander/actions-comment-pull-request@v2`.  

Тестирование: при открытии PR workflow успешно запускается, в комментариях появляется структурированное описание изменений и замечания.

### Промпт 9

**Инструмент:** Deepseek

**Промпт:**
> Добавь в тот же workflow проверку, что PR не содержит секретов (например, случайно закоммиченных `.env` или токенов).  
> Используй `gitleaks` или `trufflehog`. Если секрет найден — поставь статус `failure` и напиши предупреждение в комментарии.  
> Также добавь возможность ручного запуска (workflow_dispatch) и кэширование зависимостей Python.

**Результат:**  
Workflow дополнен:  
- шаг `gitleaks` (если секреты — exit 1)  
- кэш pip  
- триггер `workflow_dispatch`.  
Всё работает без дополнительных прав (только `contents: read` и `pull-requests: write`).

---

## 📈 Общие итоги

| Что получили                                          | Код и тесты               |
|------------------------------------------------------|---------------------------|
| ✅ Модели SQLAlchemy + асинхронная БД                | `models.py`, `database.py`|
| ✅ Аутентификация JWT + роли                         | `routers/auth.py`, `schemas.py` |
| ✅ CRUD вакансий и резюме с проверкой прав           | `routers/vacancies.py`, `routers/resumes.py` |
| ✅ Отклики с бизнес-логикой и сменой статуса         | `routers/applications.py` |
| ✅ Аналитика по вакансии                             | `routers/analytics.py`    |
| ✅ Серверные HTML-шаблоны (Jinja2)                   | `routers/frontend.py`, `templates/` |
| ✅ Полный набор pytest-тестов (95% покрытия)         | `tests/`                  |
| ✅ GitHub Actions workflow с AI-ревью PR             | `.github/workflows/pr-ai-review.yml` |

**Что пришлось исправлять вручную:**  
1. В тестах — фикстуры для async-сессий (`pytest-asyncio`).  
2. В шаблонах — передача `request` в `Jinja2Templates` для flash-сообщений.  
3. Добавление миграций Alembic после изменения моделей.  
4. В CI: корректировка прав `pull-requests: write` (изначально отсутствовало).  
5. Адаптация команды `git diff` под Windows-раннеры.

**Время разработки с AI:** ~6 часов (включая CI/CD).