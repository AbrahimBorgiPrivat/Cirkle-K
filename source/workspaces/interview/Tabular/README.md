# Tabular Automation

This folder contains Tabular Editor scripts for the `Circle K Interview` PBIP model.

## Structure

```text
Tabular/
|-- Measures/
|   `-- KPI_MEASURES/
|   `-- VISUAL_MEASURES/
|-- run_tabular_scripts.ps1
`-- README.md
```

## Requirements

- .NET 8 SDK
- Tabular Editor 2
- A local build of `source/workspaces/TabularEditorCLITool`

## Run

From the repository root or directly from this folder:

```powershell
.\source\workspaces\interview\Tabular\run_tabular_scripts.ps1
```

The PowerShell script builds the shared helper library if needed and then runs all `.csx` measure scripts for this workspace.

## Measure Coverage

- Total measures scripted: 72
- Display folders are preserved through each script entry.
- Each measure expression is stored as a separate `.dax` file for easier maintenance.
