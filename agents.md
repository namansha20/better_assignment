# Task Manager – AI Guidance File

## Project Conventions

### General
- Backend: Python 3.10+, Flask application factory pattern
- Frontend: React 18 with Vite, functional components + hooks only
- All API responses must be JSON; errors use `{"error": "message"}` format

### Backend Coding Standards
- Use SQLAlchemy ORM; never write raw SQL
- All input must be validated through marshmallow schemas before DB operations
- Status enum values: `todo`, `in_progress`, `done`
- Priority enum values: `low`, `medium`, `high`
- Hex colors must match pattern `^#[0-9A-Fa-f]{6}$`
- Use `db.session.get(Model, id)` instead of `Model.query.get(id)` (deprecated)
- All routes return proper HTTP status codes: 200, 201, 204, 400, 404, 409, 422, 500

### Frontend Coding Standards
- Use functional components and hooks (no class components)
- Inline styles only (no CSS files or CSS-in-JS libraries)
- Axios for all API calls via `src/services/api.js`
- Controlled inputs in forms

## What AI Can Do
- Add new fields to existing models (must add to schema + migration)
- Add new API endpoints following existing patterns
- Add new React components following existing style conventions
- Write new tests for new functionality

## What AI Cannot Do
- Remove existing validation from schemas
- Change enum values for status or priority without updating all dependent code
- Introduce new npm/pip dependencies without security review
- Modify the application factory pattern in app.py
- Bypass marshmallow validation in routes

## Test Requirements for AI-Generated Code
- Every new route must have a corresponding test in tests/
- Tests must cover: happy path, validation errors, not-found cases
- Use fixtures from conftest.py; do not hardcode database state
- Tests must use the TestingConfig (in-memory SQLite)

## Schema Validation Requirements
- Required fields must be marked `required=True` in marshmallow schema
- Enum fields must use `validate.OneOf([...])`
- String length limits must be enforced with `validate.Length`
- Hex color fields must use `validate.Regexp`
- All schemas must be instantiated at module level (e.g., `task_schema = TaskSchema()`)
