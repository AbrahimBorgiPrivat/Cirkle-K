# `source/code`

This folder contains the Python package, runtime definitions, and Docker services for the Circle K pipeline.

## Structure

```text
source/code/
|-- libraries/
|   |-- classes/
|   |-- runners/
|   |-- scripts/
|   `-- utils/
|-- runtime_definitions/
|-- service/
|   |-- api/
|   |-- database/
|   `-- etl/
|-- pyproject.toml
`-- poetry.lock
```

## Main Concepts

- `libraries`
Reusable Python modules used by every service.
- `runtime_definitions`
JSON-driven service configuration and SQL assets. The services read these files to decide what to run.
- `service`
Docker entrypoints for database, download, load, and simulation jobs.

## JSON Layout

Shared JSON assets are split by purpose:

- `resource/json/datafordeler`
Downloaded DAR and DAGI source files.
- `resource/json/circlek`
Static Circle K seed files used by the simulation pipeline.

## Local Poetry Setup

From `source/code`:

```powershell
poetry install
poetry run python test_poetry_script.py
```

## Environment Files

- `source/code/.envexample.txt`
Example of the shared variables used for local development and the Datafordeler download service.
- `source/code/service/*/.env.example`
Service-specific examples for the Docker-based ETL services.

The most common variables are:

- `POSTGRES_HOST`
- `POSTGRES_PORT`
- `POSTGRES_USERNAME`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`
- `DATAFORDELER_USER`
- `DATAFORDELER_PASSWORD`

## Preferred Execution Model

The preferred way to run the project is through Docker Compose files under `source/code/service/...`.

Each service starts `app/main.py`, which then:

1. loads a runtime JSON file from `runtime_definitions/<service>/runtime`
2. resolves any environment-backed values
3. executes the configured modules through a runner in `libraries.runners`

For one-shot ETL jobs, `Exited (0)` means the service completed successfully.
