#r "netstandard"
#r ".\source\workspaces\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES");
var basePath = System.IO.Path.Combine(System.Environment.CurrentDirectory, "source", "workspaces", "simulated", "Tabular", "Measures", "LOYALTY_MEASURES", "MEASURES");
var measureList = new List<string[]> {
    new[] { "Aktive Loyalty Cust.", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "Aktive Loyalty Cust.dax")), "KPI MEASURES\\LOYALTY", "", "#,0", "", "true" },
    new[] { "Loyalty Cust.", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "Loyalty Cust.dax")), "KPI MEASURES\\LOYALTY", "", "0", "", "true" },
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
