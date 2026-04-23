# Circle K Project

This repository contains the Circle K data pipelines and the Power BI workspaces built on top of them.

The project is organized around a small set of Docker-based services:

1. `source/code/service/database`
Creates the PostgreSQL/PostGIS database.
2. `source/code/service/etl/service_create_table_views_from_sql`
Creates schemas, tables, and views from SQL files in `source/code/runtime_definitions/create_table_and_views`.
3. `source/code/service/etl/service_interview_case1`
Loads the interview CSV files into the `interview` schema.
4. `source/code/service/api/service_dataformidler_download_files`
Downloads DAR and DAGI files into `resource/json`.
5. `source/code/service/etl/service_json_to_client`
Loads the downloaded DAR and DAGI JSON files into PostgreSQL.
6. `source/code/service/etl/service_simulation`
Seeds and simulates the Circle K public tables used for the reporting case.

## Repository Layout

- `docs`
Supporting documentation for both the interview case and the simulation case.
- `resource`
Shared runtime assets such as interview CSV files, downloaded JSON files, and Power BI visuals/theme files.
- `source/code`
Python package, runtime definitions, and Docker services.
- `source/workspaces`
Power BI PBIP workspaces for the interview and simulation cases.

## Recommended Run Order

Create the shared Docker network once:

```powershell
docker network create data_network
```

Then run the services in this order for the full repository setup:

```powershell
docker compose -f source\code\service\database\docker-compose.yml up -d
docker compose -f source\code\service\etl\service_create_table_views_from_sql\docker-compose.yml up --build
docker compose -f source\code\service\etl\service_interview_case1\docker-compose.yml up --build
docker compose -f source\code\service\api\service_dataformidler_download_files\docker-compose.yml up --build
docker compose -f source\code\service\etl\service_json_to_client\docker-compose.yml up --build
docker compose -f source\code\service\etl\service_simulation\docker-compose.yml up --build
```

The ETL/API services are one-shot jobs. When they finish successfully, the containers stop with `Exited (0)`. That is expected.

## Case Assets

- Interview case:
  - docs: `docs/interview`
  - csv input: `resource/csv`
  - Power BI assets: `resource/powerbi/interview`
  - PBIP workspace: `source/workspaces/interview`
- Simulation case:
  - docs: `docs/simulation`
  - json input: `resource/json/datafordeler` and `resource/json/circlek`
  - Power BI assets: `resource/powerbi/simulation`
  - PBIP workspace: `source/workspaces/simulated`

## Development Notes

- `source/code` contains the Python package and Poetry project.
- Service execution is runtime-driven through JSON files under `source/code/runtime_definitions`.
- Shared logs now use Python `logging`, so Docker logs show service progress directly.
