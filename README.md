# Team Project — Backend

REST API for the Team Project — an equipment-rental service — built with **Django + Django REST Framework**.

Frontend repository: [`team-project-frontend`](https://github.com/glor1ee/team-project-frontend)

> 🚧 **Status:** migrating the backend from FastAPI to Django + DRF.
> The scaffold is being built stage by stage — see [`DEVELOPMENT_PLAN.md`](DEVELOPMENT_PLAN.md), Stage 1.

---

## Tech stack

| Area | Choice |
| --- | --- |
| Language | Python 3.12+ |
| Framework | Django + Django REST Framework |
| Database | PostgreSQL |
| DB driver | psycopg 3 |
| Settings | django-environ (`.env`) |
| API schema | drf-spectacular (OpenAPI / Swagger) |
| Filtering | django-filter |
| CORS | django-cors-headers |
| WSGI server | Gunicorn (production) |
| Tests | pytest + pytest-django + pytest-cov |
| Lint / format | Ruff |
| Type checking | mypy |
| Hooks | pre-commit |
| CI | GitHub Actions |
| Deploy | Render |

---

## Getting started

### 1. Clone and enter the project

```bash
git clone https://github.com/glor1ee/team-project-backend.git
cd team-project-backend
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
py -3 -m venv venv
venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e ".[dev]"
```

### 4. Create the environment file

```bash
cp .env.example .env
```

`.env` is git-ignored — never commit real secrets. Point `DATABASE_URL` at a local
PostgreSQL database you have created, e.g. `easyrent`.

### 5. Apply migrations and create an admin user

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

The API is available at <http://127.0.0.1:8000>, the admin at <http://127.0.0.1:8000/admin/>.

### 7. Install git hooks (optional but recommended)

```bash
pre-commit install
```

---

## API documentation

Generated automatically by drf-spectacular:

- Swagger UI — <http://127.0.0.1:8000/api/docs/>
- OpenAPI schema — <http://127.0.0.1:8000/api/schema/>

---

## Environment variables

| Variable | Example | Description |
| --- | --- | --- |
| `DJANGO_SETTINGS_MODULE` | `config.settings.development` | Which settings module to load |
| `SECRET_KEY` | `dev-secret-change-me` | Django secret key |
| `DEBUG` | `True` | Debug mode — never `True` in production |
| `DATABASE_URL` | `postgres://postgres:postgres@localhost:5432/easyrent` | PostgreSQL connection string |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated list of allowed frontend origins |

All variables are documented in [`.env.example`](.env.example).

---

## Project structure (target)

```
team-project-backend/
├── config/                     # project configuration
│   ├── settings/
│   │   ├── base.py             # shared settings, reads .env
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py                 # root URL conf (/admin/, /api/, schema)
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── catalog/                # equipment, categories, cities, specs
│   └── bookings/               # rentals, availability, price calculation
│       └── services.py         # business logic (kept out of views)
├── tests/
├── manage.py
├── pyproject.toml              # dependencies + tool configuration
└── render.yaml                 # Render deployment blueprint
```

---

## Development commands

| Command | What it does |
| --- | --- |
| `python manage.py runserver` | Run the dev server |
| `python manage.py makemigrations` | Create migrations from model changes |
| `python manage.py migrate` | Apply migrations |
| `pytest` | Run the test suite |
| `pytest --cov --cov-report=term-missing` | Tests with a coverage report |
| `ruff check .` | Lint |
| `ruff check . --fix` | Lint and auto-fix |
| `ruff format .` | Format the code |
| `mypy .` | Static type checking |

CI runs lint, format check, type check and tests on every push and pull request to
`main` and `develop`.

---

## Git Flow

The team follows Git Flow. Two long-lived branches:

- **`main`** — production-ready code only. Never commit directly.
- **`develop`** — integration branch. All feature work merges here first.

Short-lived branches:

| Prefix | Purpose | Branch off | Merge into |
| --- | --- | --- | --- |
| `feature/*` | New functionality | `develop` | `develop` |
| `fix/*` | Bug fixes | `develop` | `develop` |
| `hotfix/*` | Urgent production fixes | `main` | `main` **and** `develop` |
| `release/*` | Release preparation | `develop` | `main` **and** `develop` |

### Typical workflow

```bash
git checkout develop
git pull origin develop

git checkout -b feature/equipment-catalog
# ... work, commit, work, commit ...
git push -u origin feature/equipment-catalog
# then open a Pull Request into develop
```

### Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add equipment list endpoint
fix: correct availability check on overlapping dates
docs: document the DATABASE_URL variable
test: cover the price calculation service
refactor: extract the booking number generator
chore: bump ruff to 0.16
```

Keep the history clean — one logical change per commit.

---

## Deployment (Render)

1. Push the repository to GitHub.
2. In Render, create a **New → Blueprint** and point it at this repository —
   [`render.yaml`](render.yaml) is picked up automatically.
3. Provision a managed PostgreSQL instance; Render injects `DATABASE_URL`.
4. Set `SECRET_KEY` and `CORS_ORIGINS` in the Render dashboard.
5. Build runs `pip install -e .` and `python manage.py migrate`;
   the service starts with `gunicorn config.wsgi`.

---

## Team

| Name | Role | GitHub |
| --- | --- | --- |
| _TBD_ | Backend | [@username](https://github.com/username) |
| _TBD_ | Frontend | [@username](https://github.com/username) |
