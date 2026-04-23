#r "netstandard"
#r ".\source\workspaces\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES");
var basePath = System.IO.Path.Combine(System.Environment.CurrentDirectory, "source", "workspaces", "simulated", "Tabular", "Measures", "REVENUE_MEASURES", "MEASURES");
var measureList = new List<string[]> {
    new[] { "LOYALITY_REVENUE", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "LOYALITY_REVENUE.dax")), "KPI MEASURES\\REVENUE", "", "#,0.00\\ \"kr.\";-#,0.00\\ \"kr.\";#,0.00\\ \"kr.\"", "", "true" },
    new[] { "AVG. REVENUE OVER TIME", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "AVG. REVENUE OVER TIME.dax")), "KPI MEASURES\\REVENUE", "", "#,0.00\\ \"kr.\";-#,0.00\\ \"kr.\";#,0.00\\ \"kr.\"", "", "true" },
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
