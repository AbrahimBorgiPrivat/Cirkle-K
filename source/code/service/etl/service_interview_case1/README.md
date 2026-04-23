# `service_interview_case1`

This one-shot ETL service loads the interview CSV files from `resource/csv` into the `interview` schema in PostgreSQL.

## Runtime

The service uses:

- runner: `libraries.runners.module_sequence`
- runtime namespace: `service_interview_case1`
- runtime file: `source/code/runtime_definitions/service_interview_case1/runtime/all.json`

The runtime executes these steps:

- Upsert Interview Item Master
- Upsert Interview Item Images
- Upsert Interview Site Master
- Upsert Interview Transactions

## Prerequisites

1. Create the Docker network:

```powershell
docker network create data_network
```

2. Start the database service.
3. Run `service_create_table_views_from_sql` with `all.json` or `interview.json`.
4. Ensure `resource/csv` contains the interview CSV files.
5. Create `.env` from `.env.example` in this folder.

## Run

From the repository root:

```powershell
docker compose -f source\code\service\etl\service_interview_case1\docker-compose.yml up --build
```

## Notes

- The service mounts only `resource/csv`, so the Docker build stays small and the CSV files are read at runtime.
- The container is expected to stop with `Exited (0)` when all interview upserts are complete.
