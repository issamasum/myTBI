# TriangleBahaiInstitute.org

The Triangle Baha’i Institute Facility supports the endevors of the Triangle Baha'i Community. It hosts many people and houses many resources. TriangleBahaiInstitute.org is a project born out the desire to have a centralized system for documenting the Facility's usage, as well as offering different resources to visitors. It is intentionally organized as a small full-stack system instead of a single app so we can work across different service boundaries, shared packages and a modern frontend.

At a high level, the system has four moving parts:

- An Angular frontend in `frontend/`
- A FastAPI HTTP adapter in `api/`
- Shared Python domain code in `packages/trianglebahaiinstitute-core/`
- Supporting development infrastructure in `.devcontainer/` and `infra/`

The repository is designed to work especially well in VS Code with the multi-root workspace file `trianglebahaiinstitute.code-workspace`.

## Quick Start

### Recommended setup: VS Code + Dev Container

1. Open `trianglebahaiinstitute.code-workspace` in VS Code.
2. Reopen the repository in the dev container when VS Code prompts you.
3. Wait for the post-create setup to finish. It installs Python dependencies with `uv`, frontend dependencies with `pnpm`, and Chromium support for Playwright UI testing.
4. Create your local environment file:
   - Run `cp .env.example .env`
   - Leave the database defaults as-is when using the dev container unless you have a specific override
5. Create the development database:
   - Run `uv run python3 packages/trianglebahaiinstitute-core/scripts/create_database.py`
   - If you need to wipe and reseed development data later, run `uv run python3 packages/trianglebahaiinstitute-core/scripts/reset_database.py`
6. Start the app stack:
   - Frontend: run the `start` task from the `frontend` workspace, or run `cd frontend && pnpm start`
   - API: run the `api: run` task from the repository workspace
7. Open the running services:
   - Frontend: `http://localhost:4200`
   - API health check: `http://localhost:8000/api/health`

## QA Quick Start

The repository-level quality gate is `scripts/qa.sh`.

- Local autofix + validation: `./scripts/qa.sh`
- CI-equivalent non-mutating check: `./scripts/qa.sh --check`

What it runs:

- Ruff formatting and linting for Python
- Pyright type checking
- Pytest with coverage across the Python workspaces, forced onto the dedicated PostgreSQL test database
- Prettier, ESLint, and Angular tests in the frontend workspace

Before `pytest`, the QA script resets the PostgreSQL test database so local runs start clean like GitHub Actions.

If you are not sure whether your work is ready, run `./scripts/qa.sh --check`. That is the closest local match to the GitHub Actions workflow.

## Deployment

## License

This repository is released under the MIT License. See `LICENSE` for the full text.

## How The Repository Is Organized

```text
.
|- api/                         FastAPI adapter layer
|- docs/                        Design notes and other documentation
|- frontend/                    Angular application
|- infra/                       Infrastructure support files
|- packages/
|  |- trianglebahaiinstitute-core/               Shared domain logic, models, services, repositories
|- scripts/                     Repository automation, including QA entrypoints
|- .devcontainer/               Recommended local development environment
|- .github/workflows/           CI workflows
|- trianglebahaiinstitute.code-workspace         VS Code multi-root workspace
```

### Architecture boundaries

- `frontend/` owns browser UI and user interaction.
- `api/` owns HTTP routes and request/response concerns.
- `packages/trianglebahaiinstitute-core/` owns shared business logic, configuration, data access, and jobs.
- `scripts/` owns repeatable repository commands, especially QA.

When we add logic, we try to put it in the deepest reusable layer that makes sense. For example, route handlers should stay thin, and shared business logic should usually live in `trianglebahaiinstitute-core` instead of in FastAPI route files.

## What Is Running Right Now?

Current source entrypoints are intentionally small so we can trace the system quickly:

- The API app is created in `api/src/api/main.py`
- Health routes live in `api/src/api/routes/health.py`
- Authentication routes live in `api/src/api/routes/auth.py`
- Shared environment-backed settings live in `packages/trianglebahaiinstitute-core/src/trianglebahaiinstitute/config.py`
- The frontend router starts in `frontend/src/app/app.routes.ts`

That means you can usually understand a feature by following this path:

1. Start in the frontend route or component.
2. Find the API endpoint it calls.
3. Trace any domain logic into `trianglebahaiinstitute-core`.

## Working In VS Code

This repository is easiest to navigate through the multi-root workspace.

### Explorer

The workspace is split into focused folders:

- `frontend`: Angular app files and frontend VS Code tasks
- `api`: FastAPI adapter code
- `core`: shared Python package from `packages/trianglebahaiinstitute-core`
- `infra`: infrastructure support files
- `repo`: repository-wide files like `.github/`, `.devcontainer/`, and `scripts/`

We use that split to decide where a change belongs before we start editing.

### Run Task

Useful task entrypoints include:

- `start` in the `frontend` workspace
- `test` in the `frontend` workspace
- `repo: uv sync` in the repository workspace
- `api: run` in the repository workspace

### Run And Debug

The repository includes launch configurations for:

- `Frontend: serve`
- `API: FastAPI`
- A workspace-level compound called `Debug Frontend + API`

If you want to understand how requests move through the system, running the debugger across all three services is a practical way to learn.

### Search And Navigation

Good first searches when you are exploring:

- Route paths in `frontend/src/app/`
- FastAPI routers in `api/src/api/routes/`
- Shared services and repositories in `packages/trianglebahaiinstitute-core/src/trianglebahaiinstitute/`
  `

## Common Development Workflows

### Frontend-only work

- Start in `frontend/src/app/`
- Run the frontend dev server
- Validate with `cd frontend && pnpm lint && pnpm test:ci`

### API or backend work

- Start in `api/src/api/` or `packages/trianglebahaiinstitute-core/src/trianglebahaiinstitute/`
- In FastAPI routes, reserve dependency injection for shared services and path-derived resources; keep request body parsing and any body-driven lookups explicit in the route.
- Validate with targeted pytest runs, then `./scripts/qa.sh --check`

### Cross-stack feature work

- Update the frontend route or component
- Update or add the API contract
- Move shared rules into `trianglebahaiinstitute-core`
- Add tests at every layer you changed

## Where To Read Next

After this README, the next documents to read are:

- `AGENTS.md` for contribution
- `api/README.md` for the FastAPI workspace
- `frontend/README.md` for the Angular workspace
- `packages/README.md` for shared package boundaries
- `scripts/README.md` for QA and automation commands

If you are brand new to the project, read them in that order.
