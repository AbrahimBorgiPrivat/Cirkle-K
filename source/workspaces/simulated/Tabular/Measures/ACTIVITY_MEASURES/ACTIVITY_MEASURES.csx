#r "netstandard"
#r ".\source\workspaces\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES");
var basePath = System.IO.Path.Combine(System.Environment.CurrentDirectory, "source", "workspaces", "simulated", "Tabular", "Measures", "ACTIVITY_MEASURES", "MEASURES");
var measureList = new List<string[]> {
    new[] { "TRANSACTIONS", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "TRANSACTIONS.dax")), "KPI MEASURES\\ACTIVITY", "", "#,0", "", "true" },
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
