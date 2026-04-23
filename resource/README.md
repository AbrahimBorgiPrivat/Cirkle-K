# Resource Directory

This folder contains shared runtime assets used by both the Python services and the Power BI workspace.

## Contents

- `json`
Downloaded source files and static seed files used by the ETL and simulation services.
- `powerbi`
Theme file and image assets used by the PBIP workspace.

## `json`

This folder is used for:

- `json/datafordeler`
Downloaded DAR and DAGI files from Datafordeler.
- `json/circlek`
Static Circle K seed files such as `CircleKCompany.json`, `PRODUCTS.json`, `CAMPAIGNS.json`, and `SEGMENTATIONSGROUPS.json`.

To populate or refresh the downloaded Datafordeler files, run:

```powershell
docker compose -f source\code\service\api\service_dataformidler_download_files\docker-compose.yml up --build
```

The download service writes into `resource/json/datafordeler` through a mounted volume.

## `powerbi`

This folder contains shared Power BI assets:

- `CirkleKPBITheme.json`
- `Images/*`

These files are referenced by the report workspace in `source/workspaces/pbip`.
