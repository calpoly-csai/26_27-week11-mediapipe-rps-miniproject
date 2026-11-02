# One-command setup for Windows (PowerShell). Clones the repo (or downloads the zip if git is
# missing), installs uv + Python 3.12 + packages, runs the checker.
#   irm https://raw.githubusercontent.com/YOUR_GITHUB_USER/rps-mediapipe/main/setup.ps1 | iex
# Also works from inside an existing clone:  .\setup.ps1
$ErrorActionPreference = "Stop"

$User = "YOUR_GITHUB_USER"
$Dir = "rps-mediapipe"
$RepoUrl = "https://github.com/$User/$Dir.git"
$ZipUrl = "https://github.com/$User/$Dir/archive/refs/heads/main.zip"

if (Test-Path "requirements.txt") {
    # already inside the project folder
} elseif ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "requirements.txt"))) {
    Set-Location $PSScriptRoot
} else {
    if (-not (Test-Path $Dir)) {
        if (Get-Command git -ErrorAction SilentlyContinue) {
            git clone $RepoUrl $Dir
            if ($LASTEXITCODE -ne 0) { throw "git clone failed" }
        } else {
            Write-Host "git not found - downloading zip instead..."
            $zip = Join-Path $env:TEMP "rps-mediapipe.zip"
            Invoke-WebRequest $ZipUrl -OutFile $zip
            Expand-Archive $zip -DestinationPath . -Force
            Rename-Item "$Dir-main" $Dir
            Remove-Item $zip
        }
    }
    Set-Location $Dir
}

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "Installing uv..."
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression
    $env:Path = "$env:USERPROFILE\.local\bin;$env:USERPROFILE\.cargo\bin;$env:Path"
}

uv venv --python 3.12 --allow-existing .venv
if ($LASTEXITCODE -ne 0) { throw "uv venv failed" }
uv pip install --python .venv\Scripts\python.exe -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "pip install failed" }
& .venv\Scripts\python.exe check_setup.py

Write-Host ""
Write-Host "Done. cd $((Get-Item .).Name) and run:  .venv\Scripts\python.exe main.py"
