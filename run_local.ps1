param(
    [switch]$SkipSeed
)

Write-Host "=== PakimonGO Local Dev Runner ===" -ForegroundColor Cyan
Write-Host ""

$ApiDir = Join-Path $PSScriptRoot "services\api"
$SrcDir = Join-Path $ApiDir "src"
$SeedDir = Join-Path $ApiDir "scripts"
$DbFile = Join-Path $ApiDir "pakimongo_dev.db"
$UploadDir = Join-Path $ApiDir "data\uploads"

$env:SYNC_DATABASE_URL = "sqlite:///$($DbFile.Replace('\','/'))"
$env:STORAGE_PROVIDER = "local"
$env:UPLOAD_BASE = $UploadDir
$env:CORS_ORIGINS = "http://localhost:5173,http://localhost:3000,http://10.0.2.2:8000"
$env:PYTHONPATH = $SrcDir

# Load gitignored local overrides (e.g. VISION_PROVIDER, GROQ_API_KEY) if present.
$EnvLocal = Join-Path $PSScriptRoot ".env.local"
if (Test-Path -LiteralPath $EnvLocal) {
    Get-Content -LiteralPath $EnvLocal | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith('#') -and $line.Contains('=')) {
            $pair = $line.Split('=', 2)
            Set-Item -Path "Env:$($pair[0].Trim())" -Value $pair[1].Trim()
        }
    }
    Write-Host "Loaded .env.local (VISION_PROVIDER=$($env:VISION_PROVIDER))" -ForegroundColor Green
}

if (-not (Test-Path -LiteralPath $UploadDir)) {
    New-Item -ItemType Directory -Path $UploadDir -Force | Out-Null
    Write-Host "Created upload directory: $UploadDir" -ForegroundColor Green
}

Write-Host "Starting API with SQLite database..." -ForegroundColor Yellow
Write-Host "  DB: $DbFile" -ForegroundColor Gray
Write-Host "  PYTHONPATH: $SrcDir" -ForegroundColor Gray
Write-Host ""

if (-not $SkipSeed) {
    Write-Host "Seeding database..." -ForegroundColor Yellow
    python -c "import sys; sys.path.insert(0, '$SrcDir'); exec(open('$SeedDir/seed.py').read())" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Seed completed (database may already have data)" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Starting uvicorn on http://localhost:8000 ..." -ForegroundColor Green
Write-Host "  Health: http://localhost:8000/health/live" -ForegroundColor Gray
Write-Host "  API:    http://localhost:8000/v1" -ForegroundColor Gray
Write-Host "  Docs:   http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "Flutter app should use: API_BASE_URL=http://localhost:8000" -ForegroundColor Cyan
Write-Host "  (Android emulator: http://10.0.2.2:8000)" -ForegroundColor Cyan
Write-Host "  (iOS simulator:   http://localhost:8000)" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop." -ForegroundColor Magenta
Write-Host ""

Set-Location -LiteralPath $ApiDir
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
