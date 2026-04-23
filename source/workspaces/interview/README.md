# Interview Workspace

This folder contains the PBIP workspace for the Circle K interview case.

## Contents

- `Circle K Interview.pbip`
The Power BI project entry file.
- `Circle K Interview.Report`
The report definition and visuals.
- `Circle K Interview.SemanticModel`
The semantic model used by the report.
- `requriement_R_packages.R`
Reference script listing the R packages required by the radar-chart part of the report.

## Related Assets

- Theme file: `resource/powerbi/interview/CirkleKPBITheme.json`
- Images: `resource/powerbi/interview/Images`
- Source CSV files: `resource/csv`
- Tabular scripts: `source/workspaces/interview/Tabular`
- Shared helper library: `source/workspaces/TabularEditorCLITool`

## Expected Data Flow

1. Run `service_create_table_views_from_sql` with the `interview` SQL runtime.
2. Run `service_interview_case1` to load the interview CSV files into PostgreSQL.
3. Open `Circle K Interview.pbip` in Power BI Desktop and point it at the loaded PostgreSQL data.

## Tabular Automation

The `Tabular` folder contains:

- DAX files for every measure currently in `_MEASURES`
- workspace-local `.csx` scripts grouped by display-folder root
- `run_tabular_scripts.ps1` for applying the scripted measures through Tabular Editor 2

The PowerShell script builds `source/workspaces/TabularEditorCLITool` automatically if the helper DLL is missing.
