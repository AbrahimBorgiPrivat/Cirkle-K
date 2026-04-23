# `libraries.scripts.api`

This package contains API-facing helper modules.

At the moment, the active module is:

- `libraries.scripts.api.dataformidler_download_files`

## `dataformidler_download_files`

This module downloads ZIP files from Datafordeler, extracts the JSON payloads, and stores the result under `resource/json/datafordeler`.

### Responsibilities

- request Datafordeler files for DAR and DAGI entities
- save ZIP payloads temporarily
- extract JSON files
- rename extracted files to the naming convention used by the ETL loaders

### Environment Requirements

The module expects:

- `DATAFORDELER_USER`
- `DATAFORDELER_PASSWORD`

These values are loaded through `libraries.utils.env`.

### Preferred Usage

This module is normally executed by the Docker service:

```powershell
docker compose -f source\code\service\api\service_dataformidler_download_files\docker-compose.yml up --build
```

### Local Usage

If you want to call it directly from `source/code`:

```powershell
poetry run python -c "from libraries.scripts.api.dataformidler_download_files import main; main()"
```
