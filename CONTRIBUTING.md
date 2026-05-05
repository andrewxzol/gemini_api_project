# Contributing

Thank you for your interest in contributing to this project. This service is a Django 5 + Django REST Framework backend that integrates with the Google Gemini API to provide AI-powered analysis capabilities, with async task processing via Celery and Redis. Contributions of all kinds — bug fixes, features, documentation, and tests — are welcome and appreciated.

## Code of Conduct

Be respectful and constructive in all interactions. Harassment, discrimination, or hostile behaviour toward other contributors will not be tolerated. If you experience or witness unacceptable behaviour, report it to the maintainers privately.

## Getting Started

**1. Clone the repository**

```bash
git clone <repository-url>
cd <repository-directory>
```

**2. Configure environment variables**

```bash
cp .env_example .env
```

Open `.env` and fill in at minimum:

- `GEMINI_API_KEY` — your Google Gemini API key
- `DEBUG` — set to `True` for local development
- `DATABASE_URL` — connection string for your Postgres instance (e.g. `postgres://user:password@localhost:5432/dbname`)

**3. Start the application**

*Docker (recommended)* — brings up Django, Postgres, Redis, and Celery in one step:

```bash
docker compose up --build
```

*Local (manual)* — requires Python 3.11 and a running Postgres and Redis instance:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Note: async tasks will not process without Celery and Redis running separately. Start Celery with:

```bash
celery -A backend worker --loglevel=info
```

## Branching and Commits

- Branch off `development` for all work.
- Use short, descriptive branch names that reflect the change:
  - `feat/add-analysis-endpoint`
  - `fix/celery-task-timeout`
  - `docs/update-contributing`
- Write commit messages in the imperative mood: "Add rate limiting to analysis view", not "Added..." or "Adding...".
- Keep each commit to one logical change.

## Pull Requests

Open all pull requests against the `development` branch. GitHub Actions runs on push to `development`, so CI will run automatically once your PR is merged.

Your PR description should include:

- What changed and why
- How to test the change manually
- Any new or changed environment variables
- Any database migrations introduced

Keep PRs focused and small — one concern per PR. Do not open a PR until CI is passing.

## Code Style

- Follow PEP 8 for all Python code. Keep line length reasonable (88 characters is acceptable).
- Respect Django app boundaries: `accounts`, `analysis`, and `api` each have a defined responsibility — avoid bleeding logic across apps.
- Prefer DRF serializers and viewsets over ad-hoc function-based views for API endpoints.
- The UI lives under `ui/templates` and `ui/static` as plain HTML, CSS, and JS — there is no Node build step, so do not introduce one.
- Never commit secrets, credentials, or your local `.env` file.

## Testing

Run the test suite before opening a PR:

```bash
python manage.py test
# or, to target the backend app specifically:
python manage.py test backend
```

Add tests for any new API endpoints or Celery tasks where practical. Tests that exercise the Gemini API should mock the external call rather than hitting the live API.

## Reporting Bugs and Requesting Features

Open a GitHub issue for both bugs and feature requests.

- **Bug report**: include steps to reproduce, expected behaviour, actual behaviour, and relevant logs or tracebacks.
- **Feature request**: describe the use case, the proposed behaviour, and any relevant API or data model implications.

## Security

Do not file public GitHub issues for security vulnerabilities. Contact the maintainers privately with a description of the issue and steps to reproduce. We will respond as quickly as possible and coordinate a fix before any public disclosure.
