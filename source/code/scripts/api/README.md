# total_downloads — Bulk File Downloader from Datafordeler API

This folder contains scripts that automate the download of ZIP files from the **Datafordeler API**, extract their contents, and organize the resulting JSON files for further processing.

These downloads include datasets from registers such as DAR and DAGI (e.g., address data, region divisions, postal codes).

## Script Overview

The script is designed to:

- Download current data snapshots for multiple entities (e.g. `Husnummer`, `Postnummer`) from Datafordeler.
- Unzip the downloaded files and extract JSON content.
- Rename the JSON files using a consistent naming convention.
- Clean up temporary files after extraction.

## Workflow

### 1. `get_api()`
- Constructs a request to the Datafordeler API using credentials and query parameters.
- Returns a streamed ZIP file response.

### 2. `download_and_unzip()`
- Downloads the ZIP file for a specific entity.
- Extracts contents and renames any `.json` files to a standardized format.
- Removes the ZIP file after extraction.

### 3. `download_files()`
- Defines a list of entity/download combinations.
- Saves extracted JSON files in `output_dir/json`.

### 4. `main()`
- Entry point for the script.
- Calls `download_files()` and defaults to using `FILES_DIR` as the target location.

## Running the Script with Poetry

Use the following command from the project root:

```bash
poetry run python total_downloads/download_datafordeler.py
```

This will download and extract all listed entities into the `files/json` folder.

## Notes

- API credentials (`DATAFORDELER_USER`, `DATAFORDELER_PASSWORD`) are imported from `utils.env` which is defined in the `.env` file.
- Output directories are configured via `utils.path_config`.
- Invalid or missing ZIP files will be caught and reported.
