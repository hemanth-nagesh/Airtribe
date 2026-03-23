# DevTrack

A tiny Django API for tracking reporters and issues. Built as a learning project — simple, readable, and easy to poke with Postman.

## Quick start

1) Create/activate your virtualenv
2) Install deps

```bash
pip install -r requriments.txt
```

3) Run the server

```bash
python manage.py runserver
```

Then open: http://127.0.0.1:8000/

## API

- `GET /api/reporters/` — list reporters
- `POST /api/reporters/` — create a reporter
- `GET /api/issues/` — list issues (supports `?id=` and `?status=`)
- `POST /api/issues/` — create an issue

Data is persisted to the local JSON files in this folder (`reporters.json`, `issues.json`).
