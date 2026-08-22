# API Workspace

This workspace contains the FastAPI adapter for TriangleBahaiInstitute.org. It owns HTTP concerns such as routing, request parsing, dependency wiring, and response models.

The API layer should stay thin. If code could be reused outside HTTP, move it into `packages/trianglebahaiinstitute-core/`.

## What Lives Here

```text
api/
|- src/api/
|  |- main.py                  FastAPI app creation
|  |- lifespan.py              Startup and shutdown wiring
|  |- di.py                    API-specific dependency factories
|  |- openapi.py               OpenAPI metadata helpers
|  |- spa.py                   SPA static-file setup
|  `- routes/                  HTTP and WebSocket route modules
|- test/                       API adapter tests
`- pyproject.toml              Package metadata
```

## Current Route Modules

All HTTP routes are mounted under `/api`.

The main route files are:

- `routes/health.py`
- `routes/auth.py`


In development mode, `routes/dev.py` adds developer-only helpers.

This is a good example of how the API workspace handles transport concerns while the backend packages handle business logic.

## How A Request Flows

Most API work follows this path:

1. Route function in `src/api/routes/`
2. API-specific dependency factory in `src/api/di.py`
3. Shared service or repository in `trianglebahaiinstitute-core`
4. Response model returned from the route

If you are debugging an endpoint, follow that path in order.

## How To Run The API

The easiest option in VS Code is the `api: run` task from the `repo` workspace.

Equivalent terminal command from the repository root:

```bash
uv run --package trianglebahaiinstitute-api uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Once it is running, check `http://localhost:8000/api/health`.

## Testing And Validation

Run API tests from the repository root:

```bash
uv run pytest api/test
```

Before finishing broader backend work, run:

```bash
./scripts/qa.sh --check
```

## Adding Or Changing An Endpoint

Use this checklist:

1. Add or update the route in `src/api/routes/`.
2. Keep HTTP-specific logic in the route or `src/api/di.py`.
3. Move reusable business logic into `trianglebahaiinstitute-core`.
4. Keep request body models explicit in the route signature.
5. Resolve body-driven lookups in the route, not in a body-derived dependency helper.
6. Add or update tests in `api/test/`, usually under `api/test/routes/`.
7. If the API contract changed, run `pnpm api:sync` from `frontend/`.

## OpenAPI Export

To export the current OpenAPI spec without starting the API server:

```bash
uv run python scripts/export_openapi.py
```

That writes `frontend/openapi.json`, which the frontend uses to regenerate its API client.

## Transaction Boundary

Database transaction lifecycle is owned by `get_session` in `trianglebahaiinstitute-core`. Route handlers must not call `session.commit()`, `session.rollback()`, or `session.begin()`.

## Good First Files To Read

If you are new to this workspace, start with:

- `src/api/main.py`
- `src/api/lifespan.py`
- `src/api/di.py`
- `src/api/routes/health.py`
- `src/api/routes/auth.py`
- `test/test_main.py`
- `test/routes/test_routes_auth.py`