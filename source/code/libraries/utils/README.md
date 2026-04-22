# `libraries.utils`

This package contains shared helpers used across all services.

## Key Modules

- `env.py`
Loads environment variables and validates required PostgreSQL and Datafordeler settings.
- `path_config.py`
Resolves shared paths such as `resource/json`, `resource`, and `runtime_definitions`. The path logic supports both repo execution and Docker execution under `/app`.
- `runtime.py`
Loads runtime JSON files and resolves environment-backed values.
- `orchestrator.py`
Shared ETL helpers for JSON loading, table validation, database reads, and bulk upserts.
- `db_types.py`
Common SQLAlchemy types used when defining table structures.
- `weights.py`
Simulation weights and configuration constants.
- `simulations_helper_functions.py`
Helper logic used by the transaction simulation modules.

## Runtime JSON Resolution

`runtime.load_runtime_vars()` reads a JSON file and resolves string values against:

1. constants already loaded in `libraries.utils.env`
2. process environment variables
3. the literal string itself if no env match is found

This is what allows the same runtime file to work across local and Docker-based runs.

## Database Helpers

`orchestrator.py` provides the shared database workflow used by the upsert modules:

- `get_data_from_db()`
- `ensure_table_structure()`
- `update_insert_dw()`
- `load_json_file()`
- `select_columns()`

These are the core building blocks behind the JSON loaders and simulation upserts.
