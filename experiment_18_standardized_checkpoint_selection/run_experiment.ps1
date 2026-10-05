param(
  [string]$RawDataDir = $env:DRIVER_DATA_RAW_DIR,
  [switch]$SkipTrain,
  [switch]$SkipEval,
  [switch]$SkipFusion,
  [switch]$SkipSummary
)

$ErrorActionPreference = "Stop"
$Here = $PSScriptRoot
$ExperimentTimer = [System.Diagnostics.Stopwatch]::StartNew()
$Python = Join-Path $Here "..\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
  $Python = "python"
}

if ([string]::IsNullOrWhiteSpace($RawDataDir)) {
  $RawDataDir = "D:\Skripsi\Experiment_TA\data\raw"
}
$env:DRIVER_DATA_RAW_DIR = $RawDataDir

Write-Host ""
Write-Host "==== $((Split-Path $Here -Leaf)) ====" -ForegroundColor Green
Write-Host "Raw data: $RawDataDir"
Write-Host "Python: $Python"

function Invoke-Step {
  param([string]$Label, [scriptblock]$Command)
  Write-Host ""
  Write-Host "---- $Label ----" -ForegroundColor Cyan
  $stepTimer = [System.Diagnostics.Stopwatch]::StartNew()
  & $Command
  $exitCode = $LASTEXITCODE
  $stepTimer.Stop()
  if ($exitCode -ne 0) {
    throw "Command failed with exit code $exitCode during $Label after $([math]::Round($stepTimer.Elapsed.TotalSeconds, 2)) sec"
  }
  Write-Host ("DONE {0} in {1} sec" -f $Label, [math]::Round($stepTimer.Elapsed.TotalSeconds, 2)) -ForegroundColor DarkGreen
}

Push-Location $Here
try {
  if (-not $SkipTrain) {
    Invoke-Step "TRAIN FRONT" { & $Python -m src.train --view front --checkpoint-monitor val_macro_f1 --early-stopping-monitor val_macro_f1 }
    Invoke-Step "TRAIN SIDE" { & $Python -m src.train --view side --checkpoint-monitor val_macro_f1 --early-stopping-monitor val_loss }
  }

  if (-not $SkipEval) {
    foreach ($split in @("train", "val", "test")) {
      Invoke-Step "EVAL FRONT $split" { & $Python -m src.evaluate --view front --split $split --checkpoint checkpoints/front/best.pt --output results/front/${split}_eval_metrics.json --predictions-output results/predictions/front_${split}_predictions.csv }
      Invoke-Step "EVAL SIDE $split" { & $Python -m src.evaluate --view side --split $split --checkpoint checkpoints/side/best.pt --output results/side/${split}_eval_metrics.json --predictions-output results/predictions/side_${split}_predictions.csv }
    }
  }

  if (-not $SkipFusion) {
    Invoke-Step "FUSION TEST" { & $Python -m src.fusion --front-checkpoint checkpoints/front/best.pt --side-checkpoint checkpoints/side/best.pt --output results/fusion/fusion_metrics.json --predictions-output results/predictions/fusion_test_predictions.csv }
  }

  if (-not $SkipSummary) {
    Invoke-Step "SUMMARY" { & $Python -m src.summarize --root . }
  }
}
finally {
  Pop-Location
  $ExperimentTimer.Stop()
  Write-Host ""
  Write-Host ("==== Completed {0} in {1} sec ====" -f (Split-Path $Here -Leaf), [math]::Round($ExperimentTimer.Elapsed.TotalSeconds, 2)) -ForegroundColor Green
}


