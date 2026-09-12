param(
  [int]$From = 1,
  [int]$To = 19,
  [string]$RawDataDir = $env:DRIVER_DATA_RAW_DIR,
  [switch]$SkipTrain,
  [switch]$SkipEval,
  [switch]$SkipFusion,
  [switch]$SkipSummary
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$TotalTimer = [System.Diagnostics.Stopwatch]::StartNew()

if ([string]::IsNullOrWhiteSpace($RawDataDir)) {
  $RawDataDir = "D:\Skripsi\Experiment_TA\data\raw"
}

for ($i = $From; $i -le $To; $i++) {
  $folder = Join-Path $Root ("experiment_{0}" -f $i)
  $expTimer = [System.Diagnostics.Stopwatch]::StartNew()
  Write-Host ""
  Write-Host "==== EXPERIMENT $i ====" -ForegroundColor Yellow
  & (Join-Path $folder "run_experiment.ps1") -RawDataDir $RawDataDir -SkipTrain:$SkipTrain -SkipEval:$SkipEval -SkipFusion:$SkipFusion -SkipSummary:$SkipSummary
  $experimentExitCode = $LASTEXITCODE
  if ($null -ne $experimentExitCode -and $experimentExitCode -ne 0) {
    throw "experiment_$i failed with exit code $experimentExitCode"
  }
  $expTimer.Stop()
  Write-Host ("==== experiment_{0} total: {1} sec ====" -f $i, [math]::Round($expTimer.Elapsed.TotalSeconds, 2)) -ForegroundColor Yellow
}

$summaryTimer = [System.Diagnostics.Stopwatch]::StartNew()
$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (Test-Path $Python) {
  & $Python scripts\build_master_summary.py
} else {
  python scripts\build_master_summary.py
}
if ($LASTEXITCODE -ne 0) {
  throw "build_master_summary.py failed with exit code $LASTEXITCODE"
}
$summaryTimer.Stop()
$TotalTimer.Stop()
Write-Host ("Master summary rebuild: {0} sec" -f [math]::Round($summaryTimer.Elapsed.TotalSeconds, 2)) -ForegroundColor Yellow
Write-Host ("All experiments finished in {0} sec" -f [math]::Round($TotalTimer.Elapsed.TotalSeconds, 2)) -ForegroundColor Yellow

