# Runs the CI pipeline stages and writes every output file into evidence\.
# Windows PowerShell version of scripts/evidence.sh. Both write the same 14 file names.
#
#   powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1
#   powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1 -Stage lint
#   powershell -ExecutionPolicy Bypass -File scripts\evidence.ps1 -Python "py -3.11"
#
# Stages, in order: prepare install lint tests semantic_layer policy security sbom pip_audit bandit checksums
# Each stage appends "<name>=<exit code>" to evidence\exit-codes.txt.
# With -Stage all (the default), a failed stage does not stop the later stages.
# The script exits 1 at the end if any stage failed. No stage switches a scan off.
#
# `opa` is not installed on most Windows machines. If it is not on the PATH, the Docker image is tried.
# If neither exists, the opa stage is recorded as not_run and opa-test.json is not written.
# Stage S04-07 Half B. PROPOSED. Owner: Team-Force.

param(
    [string]$Stage = "all",
    [string]$Python = $(if ($env:PYTHON) { $env:PYTHON } else { "python" }),
    [string]$OpaVersion = $(if ($env:OPA_VERSION) { $env:OPA_VERSION } else { "1.21.1" })
)

$ErrorActionPreference = "Continue"
$env:PIP_DISABLE_PIP_VERSION_CHECK = "1"
$env:PYTHONDONTWRITEBYTECODE = "1"

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$EV = Join-Path $Root "evidence"
$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"
$VenvScripts = Join-Path $Root ".venv\Scripts"
$OpaImage = if ($env:OPA_IMAGE) { $env:OPA_IMAGE } else { "openpolicyagent/opa:$OpaVersion" }

# $Python may hold a launcher with an argument, such as "py -3.11".
$PythonParts = $Python -split "\s+"
$PythonExe = $PythonParts[0]
$PythonArgs = @()
if ($PythonParts.Length -gt 1) { $PythonArgs = $PythonParts[1..($PythonParts.Length - 1)] }

function Record([string]$Name, $Code) { Add-Content -Path (Join-Path $EV "exit-codes.txt") -Value "$Name=$Code" -Encoding ascii }

# Write a file without a byte order mark, so the bytes match the Linux script's output.
function Write-Utf8([string]$Path, [string[]]$Lines) {
    $text = ($Lines -join "`n") + "`n"
    [System.IO.File]::WriteAllText($Path, $text, (New-Object System.Text.UTF8Encoding($false)))
}

function Stage-Prepare {
    New-Item -ItemType Directory -Force -Path $EV | Out-Null
    # Keep README.md. Remove every other file, so the secret-pattern test never reads output from an older run.
    Get-ChildItem -Path $EV -Force | Where-Object { $_.Name -ne "README.md" } | Remove-Item -Recurse -Force
    New-Item -ItemType File -Force -Path (Join-Path $EV "exit-codes.txt") | Out-Null
    $commit = (git -C $Root rev-parse HEAD 2>$null)
    if (-not $commit) { $commit = "unknown" }
    $venvPy = ""
    if (Test-Path $VenvPython) { $venvPy = (& $VenvPython --version 2>&1) }
    $sysPy = (& $PythonExe @PythonArgs --version 2>&1)
    $opaLine = "opa=not on PATH"
    if (Get-Command opa -ErrorAction SilentlyContinue) { $opaLine = "opa=" + ((opa version | Select-Object -First 1)) }
    $lines = @(
        "commit=$commit",
        ("date_utc=" + (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")),
        "runner=local",
        ("os=" + [System.Environment]::OSVersion.VersionString),
        "python_for_venv=$sysPy",
        "python_in_venv=$venvPy",
        $opaLine
    )
    Write-Utf8 (Join-Path $EV "run-info.txt") $lines
    $script:Code = 0
}

function Stage-Install {
    & powershell -ExecutionPolicy Bypass -File (Join-Path $Root "scripts\bootstrap.ps1") -Python $Python -SkipTests
    if ($LASTEXITCODE -ne 0) { $script:Code = $LASTEXITCODE; return }
    & $VenvPython -m pip install -r requirements-dev.txt
    if ($LASTEXITCODE -ne 0) { $script:Code = $LASTEXITCODE; return }
    $freeze = & $VenvPython -m pip freeze
    Write-Utf8 (Join-Path $EV "pip-freeze.txt") $freeze
    $script:Code = 0
}

function Stage-Lint {
    & $VenvPython -m ruff check apps etl legacy scripts tests semantic-layer policy --output-format json --output-file (Join-Path $EV "ruff.json")
    $script:Code = $LASTEXITCODE
}

function Stage-Tests {
    & $VenvPython -m pytest tests -m "not security" -q -p no:cacheprovider "--junitxml=$(Join-Path $EV 'junit-tests.xml')"
    $script:Code = $LASTEXITCODE
}

function Stage-SemanticLayer {
    & $VenvPython -m pytest semantic-layer/tests -q -p no:cacheprovider "--junitxml=$(Join-Path $EV 'junit-semantic-layer.xml')"
    $script:Code = $LASTEXITCODE
}

function Stage-Policy {
    & $VenvPython -m pytest policy/tests -q -p no:cacheprovider "--junitxml=$(Join-Path $EV 'junit-policy.xml')"
    $pytestCode = $LASTEXITCODE
    $opaCode = 0
    if (Get-Command opa -ErrorAction SilentlyContinue) {
        $json = & opa test policy/opa policy/tests --format json
        $opaCode = $LASTEXITCODE
        Write-Utf8 (Join-Path $EV "opa-test.json") $json
    } elseif (Get-Command docker -ErrorAction SilentlyContinue) {
        Add-Content -Path (Join-Path $EV "run-info.txt") -Value "opa_image=$OpaImage" -Encoding ascii
        $policyDir = Join-Path $Root "policy"
        $json = & docker run --rm -v "${policyDir}:/policy:ro" $OpaImage test /policy/opa /policy/tests --format json
        $opaCode = $LASTEXITCODE
        Write-Utf8 (Join-Path $EV "opa-test.json") $json
    } else {
        Write-Host "opa binary and docker are both absent. opa-test.json is not written."
        Record "opa" "not_run"
        $script:Code = $pytestCode
        return
    }
    Record "opa" $opaCode
    if ($pytestCode -ne 0) { $script:Code = $pytestCode } else { $script:Code = $opaCode }
}

function Stage-Security {
    & $VenvPython -m pytest -m security -q -p no:cacheprovider "--junitxml=$(Join-Path $EV 'junit-security.xml')"
    $pytestCode = $LASTEXITCODE
    # S05-13 SB-10. pytest exits 0 when a test is skipped. A skipped security test fails this stage.
    # The two Python-versus-Rego tests skip when `opa` is not on the PATH.
    & $VenvPython scripts/check_junit_no_skips.py (Join-Path $EV 'junit-security.xml')
    $guardCode = $LASTEXITCODE
    if ($pytestCode -ne 0) { $script:Code = $pytestCode } else { $script:Code = $guardCode }
}

function Stage-Sbom {
    # A second venv holds only requirements.txt, so the SBOM does not list the scan tools.
    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("sbom-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Force -Path $tmp | Out-Null
    $code = 1
    try {
        & $PythonExe @PythonArgs -m venv (Join-Path $tmp "venv")
        if ($LASTEXITCODE -eq 0) {
            $sbomPy = Join-Path $tmp "venv\Scripts\python.exe"
            & $sbomPy -m pip install -q -r requirements.txt
            if ($LASTEXITCODE -eq 0) {
                & (Join-Path $VenvScripts "cyclonedx-py.exe") environment --of JSON -o (Join-Path $EV "sbom.cdx.json") $sbomPy
                $code = $LASTEXITCODE
            }
        }
    } finally {
        Remove-Item -Recurse -Force $tmp -ErrorAction SilentlyContinue
    }
    $script:Code = $code
}

function Stage-PipAudit {
    & $VenvPython -m pip_audit -r requirements.txt -r requirements-dev.txt -f json -o (Join-Path $EV "pip-audit.json")
    $script:Code = $LASTEXITCODE
}

function Stage-Bandit {
    & $VenvPython -m bandit -r apps etl legacy scripts semantic-layer/build.py -f json -o (Join-Path $EV "bandit.json")
    $script:Code = $LASTEXITCODE
}

function Stage-Checksums {
    # Same order as the glob list in scripts/evidence.sh.
    $files = @()
    foreach ($pattern in @("legacy\*.py", "etl\*.py", "policy\opa\*.rego")) { $files += Get-ChildItem $pattern | Sort-Object Name }
    $files += Get-Item policy\opa\policy_data.json
    $lines = foreach ($f in $files) {
        $rel = $f.FullName.Substring($Root.Length + 1).Replace("\", "/")
        ((Get-FileHash $f.FullName -Algorithm SHA256).Hash.ToLower()) + "  " + $rel
    }
    Write-Utf8 (Join-Path $EV "source-checksums.txt") $lines
    $script:Code = 0
}

$StageNames = @("install", "lint", "tests", "semantic_layer", "policy", "security", "sbom", "pip_audit", "bandit", "checksums")
$StageFunctions = @{
    install = "Stage-Install"; lint = "Stage-Lint"; tests = "Stage-Tests"; semantic_layer = "Stage-SemanticLayer"
    policy = "Stage-Policy"; security = "Stage-Security"; sbom = "Stage-Sbom"; pip_audit = "Stage-PipAudit"
    bandit = "Stage-Bandit"; checksums = "Stage-Checksums"
}

function Run-One([string]$Name) {
    if ($Name -eq "prepare") { Stage-Prepare; return }
    if (-not (Test-Path $EV)) { New-Item -ItemType Directory -Force -Path $EV | Out-Null }
    if ($Name -ne "install" -and -not (Test-Path $VenvPython)) {
        Write-Host "evidence FAILED: $VenvPython not found. Run the install stage or scripts\bootstrap.ps1 first."
        Record $Name 127
        $script:Code = 127
        return
    }
    Write-Host "== stage $Name"
    $script:Code = 1
    & $StageFunctions[$Name]
    Record $Name $script:Code
    Write-Host "== stage $Name exit code $($script:Code)"
}

$script:Code = 0
if ($Stage -eq "all") {
    Stage-Prepare
    $failed = 0
    foreach ($s in $StageNames) {
        Run-One $s
        if ($script:Code -ne 0) { $failed++ }
    }
    Write-Host "== evidence done. Failed stages: $failed. See evidence\exit-codes.txt"
    if ($failed -ne 0) { exit 1 }
    exit 0
} elseif ($Stage -eq "prepare" -or $StageNames -contains $Stage) {
    Run-One $Stage
    exit $script:Code
} else {
    Write-Host "usage: scripts\evidence.ps1 [-Stage all|prepare|$($StageNames -join '|')]"
    exit 2
}