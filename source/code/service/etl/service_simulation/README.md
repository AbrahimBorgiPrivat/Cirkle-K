# `service_simulation`

This one-shot ETL service seeds and simulates the public Circle K tables used by the reporting case.

## Runtime

The service uses:

- runner: `libraries.runners.module_sequence`
- runtime namespace: `service_simulation`
- runtime file: `source/code/runtime_definitions/service_simulation/runtime/all.json`

The runtime executes these steps:

- Upsert Stations
- Simulate Products
- Simulate Campaign Groups
- Simulate Segmentation Groups
- Simulate Cashiers
- Simulate Customers and Cards
- Simulate Transactions

## Inputs

The service relies on seed files in `resource/json`, including:

- `CircleKCompany.json`
- `PRODUCTS.json`
- `CAMPAIGNS.json`
- `SEGMENTATIONSGROUPS.json`

## Prerequisites

1. Create the Docker network:

```powershell
docker network create data_network
```

2. Start the database service.
3. Run `service_create_table_views_from_sql`.
4. Ensure the required seed JSON files exist in `resource/json`.
5. Create `.env` from `.env.example` in this folder.

## Run

From the repository root:

```powershell
docker compose -f source\code\service\etl\service_simulation\docker-compose.yml up --build
```

## Notes

- The service writes into the public simulation tables in PostgreSQL.
- The container is expected to stop with `Exited (0)` when the simulation load is complete.
