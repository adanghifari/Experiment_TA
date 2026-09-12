param(
  [Parameter(Mandatory=$true)][int]$Seed,
  [string]$RawDataDir = $env:DRIVER_DATA_RAW_DIR
)

$ErrorActionPreference = "Stop"
$Here = $PSScriptRoot
$Python = Join-Path $Here "..\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { $Python = "python" }
if ([string]::IsNullOrWhiteSpace($RawDataDir)) { $RawDataDir = "D:\Skripsi\Experiment_TA\data\raw" }
$env:DRIVER_DATA_RAW_DIR = $RawDataDir
$env:DRIVER_TRAINING_SEED = [string]$Seed
$seedDir = "seed$Seed"

function Invoke-Step {
  param([string]$Label, [scriptblock]$Command)
  Write-Host ""
  Write-Host "---- $Label ----" -ForegroundColor Cyan
  $timer = [System.Diagnostics.Stopwatch]::StartNew()
  & $Command
  $exitCode = $LASTEXITCODE
  $timer.Stop()
  if ($exitCode -ne 0) { throw "Command failed with exit code $exitCode during $Label" }
  Write-Host ("DONE {0} in {1} sec" -f $Label, [math]::Round($timer.Elapsed.TotalSeconds, 2)) -ForegroundColor DarkGreen
}

Push-Location $Here
try {
  Write-Host "==== experiment_23 seed $Seed ====" -ForegroundColor Green
  Write-Host "Raw data: $RawDataDir"
  Write-Host "Python: $Python"

  Invoke-Step "TRAIN FRONT seed $Seed" { & $Python -m src.train --view front --checkpoint-path "checkpoints/$seedDir/front/best.pt" --history-path "results/$seedDir/front/history.json" --summary-path "results/$seedDir/front/train_summary.json" }
  Invoke-Step "TRAIN SIDE seed $Seed" { & $Python -m src.train --view side --checkpoint-path "checkpoints/$seedDir/side/best.pt" --history-path "results/$seedDir/side/history.json" --summary-path "results/$seedDir/side/train_summary.json" }

  foreach ($split in @("train", "val", "test")) {
    Invoke-Step "EVAL FRONT $split seed $Seed" { & $Python -m src.evaluate --view front --split $split --checkpoint "checkpoints/$seedDir/front/best.pt" --output "results/$seedDir/front/${split}_eval_metrics.json" --predictions-output "results/$seedDir/predictions/front_${split}_predictions.csv" }
    Invoke-Step "EVAL SIDE $split seed $Seed" { & $Python -m src.evaluate --view side --split $split --checkpoint "checkpoints/$seedDir/side/best.pt" --output "results/$seedDir/side/${split}_eval_metrics.json" --predictions-output "results/$seedDir/predictions/side_${split}_predictions.csv" }
  }

  Invoke-Step "FUSION TEST seed $Seed" { & $Python -m src.fusion --front-checkpoint "checkpoints/$seedDir/front/best.pt" --side-checkpoint "checkpoints/$seedDir/side/best.pt" --output "results/$seedDir/fusion/fusion_metrics.json" --predictions-output "results/$seedDir/predictions/fusion_test_predictions.csv" }
}
finally {
  Pop-Location
  Remove-Item Env:\DRIVER_TRAINING_SEED -ErrorAction SilentlyContinue
}
