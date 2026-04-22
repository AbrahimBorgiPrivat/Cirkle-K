# `database`

This service starts the Circle K PostgreSQL database with PostGIS enabled.

## Prerequisites

Create the shared Docker network once:

```powershell
docker network create data_network
```

Create `.env` from `.env.example` in this folder.

## Run

From the repository root:

```powershell
docker compose -f source\code\service\database\docker-compose.yml up -d
```

## What It Provides

- PostgreSQL database `circlek`
- PostGIS support through the `postgis/postgis:15-3.5` image
- persistent data via the named Docker volume `circlek_postgres_data`
- initialization SQL from `init.sql`

## Connection Defaults

The default example values are:

- database: `circlek`
- user: `postgres`
- password: `postgres`
- host port: `54321`

Inside the shared Docker network, the hostname is:

- `circlek_postgres`

## Notes

- `init.sql` runs when the database volume is initialized.
- Other services connect through the external Docker network `data_network`.
