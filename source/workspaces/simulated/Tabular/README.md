# Tabular Automation

This folder contains Tabular Editor scripts for the `Cirkle K Simulated Case` PBIP model.

## Structure

```text
Tabular/
|-- Measures/
|   |-- ACTIVITY_MEASURES/
|   |-- CAMPAIGN_MEASURES/
|   |-- LOYALTY_MEASURES/
|   `-- REVENUE_MEASURES/
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
.\source\workspaces\simulated\Tabular\run_tabular_scripts.ps1
```

The PowerShell script builds the shared helper library if needed and then runs all `.csx` measure scripts for this workspace.

## Measure Coverage

- Total measures scripted: 8
- Measures are grouped into activity, campaign, loyalty, and revenue folders.
- Each measure expression is stored as a separate `.dax` file for easier maintenance.
