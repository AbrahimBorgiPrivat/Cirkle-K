# `service_dataformidler_download_files`

This one-shot service downloads DAR and DAGI files from Datafordeler and writes them to `resource/json`.

## Runtime

The service uses:

- runner: `libraries.runners.module_sequence`
- runtime namespace: `service_dataformidler_download_files`
- runtime file: `source/code/runtime_definitions/service_dataformidler_download_files/runtime/all.json`

That runtime currently executes:

- `libraries.scripts.api.dataformidler_download_files`

## Inputs

- `source/code/.env`
Must contain `DATAFORDELER_USER` and `DATAFORDELER_PASSWORD`.
- mounted output folder: `resource`

## Run

From the repository root:

```powershell
docker compose -f source\code\service\api\service_dataformidler_download_files\docker-compose.yml up --build
```

## Output

Downloaded and extracted files are written under:

- `resource/json`

## Notes

- The service logs progress through Python `logging`.
- The container is expected to stop with `Exited (0)` when the download job is complete.
