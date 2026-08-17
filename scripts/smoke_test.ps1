param()

# Simple smoke test: start backend (uvicorn), hit /health and /gateway/plan endpoints
# Requires Python with venv activated and dependencies installed.

$env:PYTHONPATH = "$PSScriptRoot/.."
$backendPath = Join-Path $PSScriptRoot "..\services\api"

Write-Host "Starting backend for smoke test..."
Push-Location $backendPath

# Start uvicorn in background
$startInfo = New-Object System.Diagnostics.ProcessStartInfo
$startInfo.FileName = "python"
$startInfo.Arguments = "-m uvicorn services.api.main:app --host 0.0.0.0 --port 8000"
$startInfo.RedirectStandardOutput = $true
$startInfo.RedirectStandardError = $true
$startInfo.UseShellExecute = $false
$process = [System.Diagnostics.Process]::Start($startInfo)
Start-Sleep -Seconds 3

try {
    $health = Invoke-RestMethod -Uri http://localhost:8000/health -Method Get -ErrorAction Stop
    Write-Host "Health:" $health.status
    $plan = Invoke-RestMethod -Uri http://localhost:8000/plan -Method Post -Body (@{name="sample website"; domain="web"; goals=""; constraints=""; stack="fullstack"} | ConvertTo-Json) -ContentType "application/json"
    Write-Host "Plan departments:" ($plan.departments -join ", ")
} catch {
    Write-Host "Smoke test failed:" $_.Exception.Message
    exit 1
} finally {
    if ($process -and !$process.HasExited) { $process.Kill() }
    Pop-Location
}

Write-Host "Smoke test completed successfully."