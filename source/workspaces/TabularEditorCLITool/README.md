# TabularEditorCLITool

This project is the shared C# class library used by the workspace-local Tabular Editor scripts under:

- `source/workspaces/interview/Tabular`
- `source/workspaces/simulated/Tabular`

It provides reusable helpers for creating and updating:

- measures
- calculated tables
- field parameter tables
- calculation groups
- relationships
- M-code tables

## Build

From the repository root:

```powershell
dotnet build .\source\workspaces\TabularEditorCLITool\TabularEditorCLITool.csproj -c Release
```

The compiled DLL will be written to:

```text
source/workspaces/TabularEditorCLITool/bin/Release/netstandard2.0/TabularEditorCLITool.dll
```

## Usage

The workspace-level `.csx` scripts reference the DLL like this:

```csharp
#r "netstandard"
#r ".\\source\\workspaces\\TabularEditorCLITool\\bin\\Release\\netstandard2.0\\TabularEditorCLITool.dll"
using TabularEditorCLITool;
```

Each workspace `run_tabular_scripts.ps1` builds the project automatically if the DLL is missing.

## Helper Classes

- `MeasureBuilderClass.cs`
Creates and updates measures with display folders, format strings, descriptions, and optional data categories.
- `CalculatedTableBuilder.cs`
Creates DAX-based calculated tables.
- `FieldParameterBuilder.cs`
Creates field parameter tables.
- `CalculationGroupBuilder.cs`
Creates calculation groups and calculation items.
- `RelationshipBuilder.cs`
Creates or replaces relationships dynamically.
- `MCodeTableBuilder.cs`
Creates Power Query tables from M-code.

## Notes

- The project targets `netstandard2.0` and builds with the .NET 8 SDK.
- The helpers use `dynamic`, so they work against Tabular Editor 2 model objects without taking a direct dependency on internal assemblies.
