# Resource Directory

This folder contains shared runtime assets used by both the Python services and the Power BI workspace.

## Contents

- `csv`
Interview CSV files used by the case 1 ETL service.
- `json`
Downloaded source files and static seed files used by the ETL and simulation services.
- `powerbi`
Theme files and image assets used by the PBIP workspaces.

## `csv`

This folder contains the interview case source files:

- `date_dim.csv`
- `item_images.csv`
- `item_master.csv`
- `site_master.csv`
- `transactions2017.csv`
- `transactions2018.csv`

To load these files into PostgreSQL, run:

```powershell
docker compose -f source\code\service\etl\service_interview_case1\docker-compose.yml up --build
```

The service mounts `resource/csv` into the container, which keeps the Docker build context small.

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

This folder contains shared Power BI assets split by case:

- `powerbi/interview`
- `powerbi/simulation`

These files are referenced by the workspaces in `source/workspaces/interview` and `source/workspaces/simulated`.
