# One-command setup for Windows PowerShell.
# Creates .venv, installs requirements.txt, then runs pytest -q.
#
# Run from any folder:
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -Python "py -3.11"
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -SkipTests
#
# The Python name comes from -Python, then the PYTHON environment variable, then "python".
# The script exits with a non-zero code when any step fails.
# Stage S04-05 Half B. PROPOSED. Owner: Team-Force.

param(
    [string]$Python = $(if ($env:PYTHON) { $env:PYTHON } else { "python" }),
    [switch]$SkipTests
)

# Native commands do not stop the script by themselves. Each step checks its exit code.
$ErrorActionPreference = "Continue"
$env:PIP_DISABLE_PIP_VERSION_CHECK = "1"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

function Stop-Setup([string]$Message, [int]$Code) {
    Write-Host "bootstrap FAILED: $Message"
    exit $Code
}

# $Python may hold a launcher with an argument, such as "py -3.11".
$PythonParts = $Python -split "\s+"
$PythonExe = $PythonParts[0]
$PythonArgs = @()
if ($PythonParts.Length -gt 1) { $PythonArgs = $PythonParts[1..($PythonParts.Length - 1)] }

Write-Host "== Step 1 of 4: check Python"
& $PythonExe @PythonArgs --version
if ($LASTEXITCODE -ne 0) { Stop-Setup "Python command '$Python' did not run. Set -Python or the PYTHON variable." 1 }
& $PythonExe @PythonArgs -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if ($LASTEXITCODE -ne 0) { Stop-Setup "Python 3.10 or newer is needed. CI uses 3.11." 1 }

Write-Host "== Step 2 of 4: create .venv"
if (Test-Path $VenvPython) {
    Write-Host ".venv already exists. Reusing it."
} else {
    & $PythonExe @PythonArgs -m venv (Join-Path $Root ".venv")
    if ($LASTEXITCODE -ne 0) { Stop-Setup "could not create .venv" 2 }
}
& $VenvPython --version

Write-Host "== Step 3 of 4: install requirements.txt"
& $VenvPython -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Stop-Setup "pip install failed" 3 }

if ($SkipTests) {
    Write-Host "== Step 4 of 4: skipped (-SkipTests)"
    Write-Host "bootstrap OK (tests skipped)"
    exit 0
}

Write-Host "== Step 4 of 4: run pytest -q"
& $VenvPython -m pytest -q
if ($LASTEXITCODE -ne 0) { Stop-Setup "pytest reported a failure (exit code $LASTEXITCODE)" 4 }

Write-Host "bootstrap OK"
exit 0
