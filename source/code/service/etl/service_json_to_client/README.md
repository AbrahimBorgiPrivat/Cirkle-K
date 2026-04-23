# `service_json_to_client`

This one-shot ETL service loads the DAR and DAGI JSON files from `resource/json/datafordeler` into PostgreSQL.

## Runtime

The service uses:

- runner: `libraries.runners.module_sequence`
- runtime namespace: `service_json_to_client`
- runtime file: `source/code/runtime_definitions/service_json_to_client/runtime/all.json`

The runtime executes the upsert modules for:

- DAGI Kommuneinddeling
- DAGI Landsdel
- DAGI Postnummerinddeling
- DAGI Region
- DAGI Storkreds
- DAR Adresse
- DAR Adressepunkt
- DAR Husnummer
- DAR Navngivenvej
- DAR Postnummer

## Prerequisites

1. Create the Docker network:

```powershell
docker network create data_network
```

2. Start the database service.
3. Run `service_create_table_views_from_sql`.
4. Ensure `resource/json/datafordeler` contains the downloaded DAR and DAGI files.
5. Create `.env` from `.env.example` in this folder.

## Run

From the repository root:

```powershell
docker compose -f source\code\service\etl\service_json_to_client\docker-compose.yml up --build
```

## Notes

- The service mounts only `resource/json/datafordeler` into the container to keep the runtime payload smaller.
- The container is expected to stop with `Exited (0)` when all upserts are complete.
