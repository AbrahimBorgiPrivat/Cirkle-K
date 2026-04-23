# Simulated Workspace

This folder contains the PBIP workspace for the Circle K simulated case.

## Contents

- `Cirkle K Simulated Case.pbip`
The Power BI project entry file.
- `Cirkle K Simulated Case.Report`
The report definition and visuals.
- `Cirkle K Simulated Case.SemanticModel`
The semantic model used by the report.
- `Tabular`
Tabular Editor scripts and per-measure DAX files for the `_MEASURES` table.

## Related Assets

- Theme file: `resource/powerbi/simulation/CirkleKPBITheme.json`
- Images: `resource/powerbi/simulation/Images`
- Seed JSON files: `resource/json/circlek`
- Shared helper library: `source/workspaces/TabularEditorCLITool`

## Expected Data Flow

1. Run `service_create_table_views_from_sql`.
2. Run `service_dataformidler_download_files` and `service_json_to_client` if the model depends on Datafordeler-loaded tables.
3. Run `service_simulation` to generate the simulated public tables.
4. Open `Cirkle K Simulated Case.pbip` in Power BI Desktop and point it at the loaded PostgreSQL data.

## Tabular Automation

The `Tabular` folder contains:

- DAX files for every measure currently in `_MEASURES`
- a workspace-local `.csx` script
- `run_tabular_scripts.ps1` for applying the scripted measures through Tabular Editor 2

The PowerShell script builds `source/workspaces/TabularEditorCLITool` automatically if the helper DLL is missing.
