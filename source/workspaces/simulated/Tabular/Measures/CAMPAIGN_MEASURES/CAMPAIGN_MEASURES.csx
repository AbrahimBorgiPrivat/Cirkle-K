#r "netstandard"
#r ".\source\workspaces\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES");
var basePath = System.IO.Path.Combine(System.Environment.CurrentDirectory, "source", "workspaces", "simulated", "Tabular", "Measures", "CAMPAIGN_MEASURES", "MEASURES");
var measureList = new List<string[]> {
    new[] { "USED CAMPAIGNS", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "USED CAMPAIGNS.dax")), "KPI MEASURES\\CAMPAIGNS", "", "#,0", "", "true" },
    new[] { "USER USED CAMPAIGNS", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "USER USED CAMPAIGNS.dax")), "KPI MEASURES\\CAMPAIGNS", "", "#,0", "", "true" },
    new[] { "(%) USER USED CAMPAIGNS", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "(%) USER USED CAMPAIGNS.dax")), "KPI MEASURES\\CAMPAIGNS", "", "0.00\\ %;-0.00\\ %;0.00\\ %", "", "true" },
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
