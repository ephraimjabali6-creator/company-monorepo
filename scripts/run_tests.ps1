# Cross-language test runner (Windows PowerShell)
$here = Split-Path -Parent $MyInvocation.MyCommand.Definition
$repoRoot = Join-Path $here ".."
$venvPath = Join-Path $repoRoot ".venv"
Write-Output "Running basic validations..."

# Python tests
if (Get-Command python -ErrorAction SilentlyContinue) {
  Write-Output "Running Python tests"
  if (-not (Test-Path $venvPath)) {
    python -m venv $venvPath
  }
  $py = Join-Path $venvPath "Scripts\python.exe"
  & $py -m pip install -r (Join-Path $repoRoot "services\api\requirements.txt") | Out-Null
  Push-Location $repoRoot
  try {
    & $py -m pytest -q services/api/tests company/tests
  } catch {
    Write-Output "Python tests failed."
  }
  Pop-Location
} else {
  Write-Output "Python not found -- skip Python tests"
}

# Go tests
if (Get-Command go -ErrorAction SilentlyContinue) {
  Write-Output "Running Go tests"
  Push-Location (Join-Path $repoRoot "services\go")
  try {
    & go test ./...
  } catch {
    Write-Output "Go tests failed (non-zero exit)"
  }
  Pop-Location
} else { Write-Output "Go not found -- skip Go tests" }

Write-Output "All done. See each service output for failures."