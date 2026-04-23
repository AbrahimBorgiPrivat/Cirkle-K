#r "netstandard"
#r ".\source\workspaces\TabularEditorCLITool\bin\Release\netstandard2.0\TabularEditorCLITool.dll"
using TabularEditorCLITool;

var calctable = MeasureBuilder.CheckTable(Model, "_MEASURES");
var basePath = System.IO.Path.Combine(System.Environment.CurrentDirectory, "source", "workspaces", "interview", "Tabular", "Measures", "VISUAL_MEASURES", "MEASURES");
var measureList = new List<string[]> {
    new[] { "SelectedMetricTitle", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "SelectedMetricTitle.dax")), "VISUAL MEASURES\\TITLES", "", "", "", "true" },
    new[] { "Title_Period", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "Title_Period.dax")), "VISUAL MEASURES\\TITLES", "", "", "", "true" },
    new[] { "Title_Product", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "Title_Product.dax")), "VISUAL MEASURES\\TITLES", "", "", "", "true" },
    new[] { "Title_AreaSite", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "Title_AreaSite.dax")), "VISUAL MEASURES\\TITLES", "", "", "", "true" },
    new[] { "Title_Tree", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "Title_Tree.dax")), "VISUAL MEASURES\\TITLES", "", "", "", "true" },
    new[] { "TOP1 SELLING ITEM IMAGE URL", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "TOP1 SELLING ITEM IMAGE URL.dax")), "VISUAL MEASURES\\IMAGES", "", "", "ImageUrl", "true" },
    new[] { "TOP1 SELLING ITEM", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "TOP1 SELLING ITEM.dax")), "VISUAL MEASURES\\IMAGES", "", "", "", "true" },
    new[] { "TOP2 SELLING ITEM IMAGE URL", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "TOP2 SELLING ITEM IMAGE URL.dax")), "VISUAL MEASURES\\IMAGES", "", "", "", "true" },
    new[] { "TOP2 SELLING ITEM", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "TOP2 SELLING ITEM.dax")), "VISUAL MEASURES\\IMAGES", "", "", "", "true" },
    new[] { "TOP3 SELLING ITEM IMAGE URL", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "TOP3 SELLING ITEM IMAGE URL.dax")), "VISUAL MEASURES\\IMAGES", "", "", "", "true" },
    new[] { "TOP3 SELLING ITEM", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "TOP3 SELLING ITEM.dax")), "VISUAL MEASURES\\IMAGES", "", "", "", "true" },
    new[] { "HTML_EXPLENATION_PAGE_OVERVIEW", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "HTML_EXPLENATION_PAGE_OVERVIEW.dax")), "VISUAL MEASURES\\PAGE EXPLENATIONS", "", "", "", "true" },
    new[] { "HTML_EXPLENATION_PAGE_COMPARE_SITE", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "HTML_EXPLENATION_PAGE_COMPARE_SITE.dax")), "VISUAL MEASURES\\PAGE EXPLENATIONS", "", "", "", "true" },
    new[] { "HTML_EXPLENATION_PAGE_DRIVERTREE", System.IO.File.ReadAllText(System.IO.Path.Combine(basePath, "HTML_EXPLENATION_PAGE_DRIVERTREE.dax")), "VISUAL MEASURES\\PAGE EXPLENATIONS", "", "", "", "true" },
};
MeasureBuilder.AddMultipleFormattedMeasures(Model, calctable, measureList);
