$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$Target = Join-Path $Root "docs\chapters-en"
$Source = Join-Path $Root "chapters-en"
if (Test-Path $Target) { Remove-Item $Target -Recurse -Force }
Copy-Item $Source $Target -Recurse
Copy-Item (Join-Path $Root "CONTRIBUTING.md") (Join-Path $Root "docs\contributing.md") -Force
Write-Host "Prepared docs/chapters-en and docs/contributing.md"
