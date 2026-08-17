# Cross-language test runner (Windows PowerShell)
$here = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Output "Running basic validations..."

# Python tests
if (Get-Command python -ErrorAction SilentlyContinue) {
  Write-Output "Running Python tests"
  python -m pip install -r "$here\..\services\api\requirements.txt" | Out-Null
  pushd "$here\..\services\api"; pytest -q tests; popd
} else {
  Write-Output "Python not found -- skip Python tests"
}

# Go tests
if (Get-Command go -ErrorAction SilentlyContinue) {
  Write-Output "Running Go tests"
  pushd "$here\..\services\go"
  try {
    & go test ./...
  } catch {
    Write-Output "Go tests failed (non-zero exit)"
  }
  popd
} else { Write-Output "Go not found -- skip Go tests" }

Write-Output "All done. See each service output for failures."