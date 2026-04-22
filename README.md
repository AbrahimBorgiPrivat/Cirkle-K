# Circle K Project

This repository contains the Circle K data pipeline and the Power BI workspace built on top of it.

The project is organized around a small set of Docker-based services:

1. `source/code/service/database`
Creates the PostgreSQL/PostGIS database.
2. `source/code/service/etl/service_create_table_views_from_sql`
Creates schemas, tables, and views from SQL files in `source/code/runtime_definitions/create_table_and_views`.
3. `source/code/service/api/service_dataformidler_download_files`
Downloads DAR and DAGI files into `resource/json`.
4. `source/code/service/etl/service_json_to_client`
Loads the downloaded DAR and DAGI JSON files into PostgreSQL.
5. `source/code/service/etl/service_simulation`
Seeds and simulates the Circle K public tables used for the reporting case.

## Repository Layout

- `docs`
Project notes and supporting documentation.
- `resource`
Shared runtime assets such as downloaded JSON files and Power BI visuals/theme files.
- `source/code`
Python package, runtime definitions, and Docker services.
- `source/workspaces`
Power BI PBIP workspace.

## Recommended Run Order

Create the shared Docker network once:

```powershell
docker network create data_network
```

Then run the services in this order:

```powershell
docker compose -f source\code\service\database\docker-compose.yml up -d
docker compose -f source\code\service\etl\service_create_table_views_from_sql\docker-compose.yml up --build
docker compose -f source\code\service\api\service_dataformidler_download_files\docker-compose.yml up --build
docker compose -f source\code\service\etl\service_json_to_client\docker-compose.yml up --build
docker compose -f source\code\service\etl\service_simulation\docker-compose.yml up --build
```

The ETL/API services are one-shot jobs. When they finish successfully, the containers stop with `Exited (0)`. That is expected.

## Power BI Workspace

The PBIP project lives under `source/workspaces/pbip`.

Shared report assets such as theme and images live under `resource/powerbi`.

## Development Notes

- `source/code` contains the Python package and Poetry project.
- Service execution is runtime-driven through JSON files under `source/code/runtime_definitions`.
- Shared logs now use Python `logging`, so Docker logs show service progress directly.
