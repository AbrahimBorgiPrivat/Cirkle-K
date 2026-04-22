# `service_create_table_views_from_sql`

This one-shot ETL service creates and refreshes schemas, tables, and views from SQL files stored under `source/code/runtime_definitions/create_table_and_views`.

## Runtime Inputs

- runtime JSON files:
  - `all.json`
  - `datafordeler.json`
  - `default_data.json`
  - `interview.json`
  - `public.json`
- SQL files under:
  - `source/code/runtime_definitions/create_table_and_views/queries`

The default runtime file is `all.json`.

## Execution Model

The service uses:

- runner: `libraries.runners.create_table_and_views_from_sql`
- runtime namespace: `create_table_and_views`

For each SQL file in the selected runtime JSON, the runner reads the file from the mounted path under `/app/runtime_definitions/create_table_and_views/...` and executes it against PostgreSQL.

## Prerequisites

1. Create the Docker network:

```powershell
docker network create data_network
```

2. Start the database service.
3. Create `.env` from `.env.example` in this folder.

## Run

From the repository root:

```powershell
docker compose -f source\code\service\etl\service_create_table_views_from_sql\docker-compose.yml up --build
```

## Selecting a Runtime File

Set `RUNTIME_FILES` in this service's `.env` file to choose a different runtime payload, for example:

- `all.json`
- `public.json`
- `datafordeler.json`

## Regenerating SQL Definitions

`app/export_live_schema.py` can regenerate the SQL snapshot and runtime JSON files from a live database.

## Notes

- The service is expected to stop with `Exited (0)` when all SQL files have been applied successfully.
- `queries/migration/001_postgis.sql` handles the PostGIS extension setup.
