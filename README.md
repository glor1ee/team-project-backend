# Team Project — Backend

REST API for the Team Project, built with **FastAPI**.

Frontend repository: [`team-project-frontend`](https://github.com/glor1ee/team-project-frontend)

---

## Tech stack

| Area | Choice |
| --- | --- |
| Language | Python 3.12+ |
| Framework | FastAPI |
| ASGI server | Uvicorn |
| Settings | pydantic-settings |
| Tests | pytest + pytest-cov |
| Lint / format | Ruff |
| Type checking | mypy (strict) |
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
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -e ".[dev]"
```

### 4. Create the environment file

```bash
cp .env.example .env
```

`.env` is git-ignored — never commit real secrets.

### 5. Run the server

```bash
uvicorn app.main:app --reload
```

The API is now available at <http://127.0.0.1:8000>.

### 6. Install git hooks (optional but recommended)

```bash
pre-commit install
```

---

## Sanity check

```bash
curl http://127.0.0.1:8000/api/hello
# {"message":"Hello world!"}
```

---

## API endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Root sanity endpoint — returns `Hello world!` |
| `GET` | `/api/hello` | Sanity endpoint — returns `Hello world!` |
| `GET` | `/api/health` | Health probe used by CI and by Render |

Interactive documentation is generated automatically:

- Swagger UI — <http://127.0.0.1:8000/docs>
- ReDoc — <http://127.0.0.1:8000/redoc>
- OpenAPI schema — <http://127.0.0.1:8000/openapi.json>

---

## Environment variables

| Variable | Default | Description |
| --- | --- | --- |
| `APP_NAME` | `Team Project API` | Title shown in the OpenAPI docs |
| `ENVIRONMENT` | `development` | Environment label (`development` / `production`) |
| `DEBUG` | `true` | Enables FastAPI debug mode |
| `CORS_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | Comma-separated list of allowed frontend origins |

All variables are documented in [`.env.example`](.env.example).

---

## Project structure

```
team-project-backend/
├── app/
│   ├── api/
│   │   └── routes.py       # API routers
│   ├── config.py           # Settings loaded from env / .env
│   └── main.py             # App factory + ASGI entry point
├── tests/
│   └── test_main.py        # Endpoint tests
├── .github/
│   ├── workflows/ci.yml    # Lint, type-check, test on every push/PR
│   └── pull_request_template.md
├── .env.example
├── .pre-commit-config.yaml
├── pyproject.toml          # Dependencies + tool configuration
└── render.yaml             # Render deployment blueprint
```

---

## Development commands

| Command | What it does |
| --- | --- |
| `uvicorn app.main:app --reload` | Run the dev server with hot reload |
| `pytest` | Run the test suite |
| `pytest --cov=app --cov-report=term-missing` | Tests with a coverage report |
| `ruff check .` | Lint |
| `ruff check . --fix` | Lint and auto-fix |
| `ruff format .` | Format the code |
| `mypy app` | Static type checking |

CI runs all of these on every push and pull request to `main` and `develop`.

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

git checkout -b feature/user-authentication
# ... work, commit, work, commit ...
git push -u origin feature/user-authentication
# then open a Pull Request into develop
```

### Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add user registration endpoint
fix: correct pagination offset on the items list
docs: document the CORS_ORIGINS variable
test: cover the health endpoint
refactor: extract the settings object
chore: bump ruff to 0.8.4
```

Keep the history clean — one logical change per commit.

---

## Deployment (Render)

1. Push the repository to GitHub.
2. In Render, create a **New → Blueprint** and point it at this repository — [`render.yaml`](render.yaml) is picked up automatically.
3. Set `CORS_ORIGINS` in the Render dashboard to the deployed frontend URL.
4. Render builds with `pip install -e .` and starts `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
5. Health checks hit `/api/health`.

---

## Team

| Name | Role | GitHub |
| --- | --- | --- |
| _TBD_ | Backend | [@username](https://github.com/username) |
| _TBD_ | Frontend | [@username](https://github.com/username) |
