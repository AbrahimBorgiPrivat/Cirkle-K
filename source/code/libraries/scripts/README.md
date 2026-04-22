# `libraries.scripts`

This package contains the business modules that the services execute.

These modules are usually not started directly in production. Instead, Docker services load runtime JSON files and call the modules through `libraries.runners.module_sequence`.

## Package Layout

- `api`
Download and extract external files.
- `pipelines`
Convenience orchestration scripts for local/manual runs.
- `simulations`
Data generation logic used by the simulation upserts.
- `upserts`
Modules that create or update database tables from JSON files or generated data.

## Runtime-Driven Execution

Most services use this pattern:

1. `app/main.py` loads `runtime_definitions/<service>/runtime/all.json`
2. `libraries.runners.module_sequence` iterates over `modules`
3. each configured script module is imported and its `main()` function is called

That keeps service flow configurable without changing Python entrypoints.

## Local Convenience Scripts

The `pipelines` folder is still useful for local development, but it is no longer the primary deployment path.

Examples:

```powershell
cd source\code
poetry run python libraries\scripts\pipelines\datafordeler_main.py
poetry run python libraries\scripts\pipelines\cirkleKsimulations.py
```

## Logging

Scripts now use Python `logging`, so their progress appears in Docker logs without relying on `print`.
