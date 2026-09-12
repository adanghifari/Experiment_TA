$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install -r requirements.txt

