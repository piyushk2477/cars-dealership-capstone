# fullstack_developer_capstone

Full-stack car dealership review application built with **Django REST-style views** and a React frontend. This repository is the working source project for the 28-task capstone checklist.

## Features
- Django server and JSON API
- Dealer directory, dealer detail, dealer reviews, and state filtering
- User registration, login, and logout endpoints
- Review submission and sentiment analysis hook
- Static About and Contact pages
- React registration component
- Docker-ready local development and GitHub Actions CI

> **Important:** Evidence screenshots and a deployed URL must be captured from a real running application and deployment. The repository does not fabricate screenshots, terminal output, or a deployment URL.

## Quick start (backend)
Python 3.11+ recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate --run-syncdb
python manage.py seed_dealers
python manage.py runserver
```

Open http://127.0.0.1:8000/ and test API endpoints below. The landing page is served by Django. To run the React UI in development, open a second terminal:

```bash
cd server/frontend
npm install
npm run dev
```

Visit http://localhost:5173. Vite proxies `/djangoapp` API requests to Django at port 8000. Create an admin account with `python manage.py createsuperuser` to manage dealers at `/admin/`.

## API endpoints
- `GET /djangoapp/get_dealers`
- `GET /djangoapp/get_dealers?state=TX`
- `GET /djangoapp/get_dealer_by_id/<dealer_id>`
- `GET /djangoapp/get_dealer_reviews/<dealer_id>`
- `GET /djangoapp/get_dealers_by_state/<state>`
- `GET /djangoapp/get_cars`
- `GET /djangoapp/get_all_car_makes`
- `POST /djangoapp/register`
- `POST /djangoapp/login`
- `POST /djangoapp/logout`
- `POST /djangoapp/add_review`
- `POST /djangoapp/analyze_review`

## Task evidence checklist
See [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md) for the expected artifact names and what must be captured after running/deploying the project.

## Configuration
Copy `.env.example` to `.env` for local settings if needed. Never commit passwords, API keys, or production secrets.
