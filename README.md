# Task Manager

A full-stack task management application built with Python/Flask (backend) and React/Vite (frontend).

## Architecture Overview

```
├── backend/          # Flask REST API
│   ├── app.py        # Application factory
│   ├── config.py     # Configuration classes
│   ├── extensions.py # SQLAlchemy instance (avoids circular imports)
│   ├── models.py     # SQLAlchemy ORM models
│   ├── schemas.py    # Marshmallow validation/serialization schemas
│   ├── routes/       # Blueprint-based route handlers
│   └── tests/        # pytest test suite
└── frontend/         # React + Vite SPA
    └── src/
        ├── App.jsx
        ├── components/
        └── services/api.js
```

## Key Technical Decisions

| Decision | Rationale |
|----------|-----------|
| **Flask** | Lightweight, composable, ideal for REST APIs; application factory pattern enables testing isolation |
| **SQLite + SQLAlchemy** | Zero-config relational DB for local dev; ORM prevents SQL injection; easy to swap to PostgreSQL |
| **marshmallow** | Declarative schema validation and serialization; keeps validation logic out of route handlers |
| **React + Vite** | Fast HMR, minimal config, modern JSX transform; functional components + hooks for simplicity |
| **In-memory SQLite for tests** | Fast, isolated, no file cleanup needed between test runs |

## How to Run

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
# API available at http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# App available at http://localhost:5173
```

## API Documentation

### Health
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |

### Tasks
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/tasks` | List all tasks (filter: `?status=`, `?priority=`, `?category_id=`) |
| POST | `/api/tasks` | Create a task |
| GET | `/api/tasks/<id>` | Get a task |
| PUT | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |

### Categories
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/categories` | List all categories |
| POST | `/api/categories` | Create a category |
| GET | `/api/categories/<id>` | Get a category |
| DELETE | `/api/categories/<id>` | Delete a category |

**Task fields:** `title` (required), `description`, `status` (todo/in_progress/done), `priority` (low/medium/high), `due_date` (YYYY-MM-DD), `category_id`

**Category fields:** `name` (required), `color` (hex, default `#6366f1`)

## Testing

```bash
cd backend
pip install -r requirements.txt
python -m pytest tests/ -v
```

## AI Usage

This project was scaffolded with AI assistance (GitHub Copilot). The `agents.md` file documents what AI can and cannot modify in this codebase, coding conventions, and test requirements for AI-generated code.

## Known Limitations / Tradeoffs

- **No authentication**: All tasks/categories are globally accessible. Add Flask-JWT-Extended for multi-user support.
- **SQLite concurrency**: SQLite has limited write concurrency; switch to PostgreSQL for production.
- **No pagination**: Task list is unbounded; add limit/offset or cursor pagination for large datasets.
- **Frontend no routing**: Single-page with no URL routing; add React Router for better UX.
- **Inline styles**: No CSS framework; easier to read but harder to maintain at scale.