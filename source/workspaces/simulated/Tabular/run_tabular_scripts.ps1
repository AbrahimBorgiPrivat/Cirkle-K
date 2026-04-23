# ============================================
# Run Tabular Editor scripts sequentially
# ============================================

$tabularEditorPath = "C:\Program Files (x86)\Tabular Editor\TabularEditor.exe"
if (-not (Test-Path $tabularEditorPath)) {
    Write-Host "Error: The path to TabularEditor.exe is incorrect or the file does not exist." -ForegroundColor Red
    Write-Host "Expected path: $tabularEditorPath"
    exit 1
}

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..\..\..')
Set-Location $repoRoot

$workspaceRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$modelPath = Join-Path $workspaceRoot 'Cirkle K Simulated Case.SemanticModel\definition\database.tmdl'
if (-not (Test-Path $modelPath)) {
    Write-Host "Error: The model path (.tmdl) does not exist or is invalid." -ForegroundColor Red
    Write-Host "Expected path: $modelPath"
    exit 1
}

$toolProjectDir = Join-Path $repoRoot 'source\workspaces\TabularEditorCLITool'
$toolDllPath = Join-Path $toolProjectDir 'bin\Release\netstandard2.0\TabularEditorCLITool.dll'
if (-not (Test-Path $toolDllPath)) {
    Write-Host "Building TabularEditorCLITool..." -ForegroundColor Cyan
    dotnet build (Join-Path $toolProjectDir 'TabularEditorCLITool.csproj') -c Release
}
if (-not (Test-Path $toolDllPath)) {
    Write-Host "Error: TabularEditorCLITool.dll could not be found after build." -ForegroundColor Red
    Write-Host "Expected path: $toolDllPath"
    exit 1
}

$scriptsBase = Resolve-Path $PSScriptRoot
$scripts = @(
    "$scriptsBase\Measures\REVENUE_MEASURES\REVENUE_MEASURES.csx",
    "$scriptsBase\Measures\ACTIVITY_MEASURES\ACTIVITY_MEASURES.csx",
    "$scriptsBase\Measures\LOYALTY_MEASURES\LOYALTY_MEASURES.csx",
    "$scriptsBase\Measures\CAMPAIGN_MEASURES\CAMPAIGN_MEASURES.csx"
)

foreach ($script in $scripts) {
    Write-Host "Running script: $script" -ForegroundColor Cyan
    if (-not (Test-Path $script)) {
        Write-Host "Error executing: $script (file not found)" -ForegroundColor Red
        continue
    }
    $output = (& $tabularEditorPath $modelPath -S $script -D 2>&1 | Out-String).Trim()
    Write-Host $output
    if ($output -match 'Model metadata saved') {
        Write-Host "Completed: $script" -ForegroundColor Green
    } else {
        Write-Host "Warning: Could not confirm success for $script" -ForegroundColor Yellow
    }
}

Write-Host "All scripts executed!" -ForegroundColor Green
