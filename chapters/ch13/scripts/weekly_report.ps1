# Dana's weekly report with nobody at the keyboard. Exit 0 means a fresh report exists and nothing was refused.
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)   # the project root, wherever the scheduler started this script
New-Item -ItemType Directory -Force out | Out-Null
$started = Get-Date

$json = claude -p "/weekly-report" `
    --model haiku `
    --max-turns 15 `
    --output-format json `
    --permission-mode dontAsk `
    --allowedTools "Skill" `
    --strict-mcp-config
$exit = $LASTEXITCODE
if (-not $json) { Write-Error "claude printed nothing (exit $exit)"; exit 1 }
$json | Set-Content -Encoding utf8 out\weekly_report.json

$result = $json | ConvertFrom-Json
$denied = @($result.permission_denials).Count
$report = Get-ChildItem reports\kpi-*.md -ErrorAction SilentlyContinue | Sort-Object Name | Select-Object -Last 1
$net = if ($report) { Select-String -Path $report.FullName -Pattern '^\| Net sales' | Select-Object -First 1 }

if ($exit -ne 0 -or $result.is_error -or $denied -gt 0 -or -not $report -or $report.LastWriteTime -lt $started -or -not $net) {
    Write-Error "weekly report failed: exit $exit, is_error $($result.is_error), $denied refusals, report $($report.Name)"
    exit 1
}
"$($report.Name): $($net.Line)"
exit 0
