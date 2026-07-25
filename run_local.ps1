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

# Preflight: `python` on PATH can resolve to an unrelated environment (a
# different tool's virtualenv, etc.) that is missing this API's
# dependencies. That used to fail the seed step below silently - see
# docs/BUGS_AND_RISKS.md - so check for it up front with a clear message
# instead of a buried traceback.
python -c "import fastapi, sqlalchemy, uvicorn" 2>$null
if ($LASTEXITCODE -ne 0) {
    $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
    Write-Host "ERROR: 'python' ($pythonPath) is missing fastapi/sqlalchemy/uvicorn." -ForegroundColor Red
    Write-Host "  Install them with: pip install -r services/api/requirements.txt" -ForegroundColor Red
    Write-Host "  or activate the environment that already has them first." -ForegroundColor Red
    exit 1
}

if (-not $SkipSeed) {
    Write-Host "Seeding database..." -ForegroundColor Yellow
    $seedOutput = python -c "import sys; sys.path.insert(0, '$SrcDir'); exec(open('$SeedDir/seed.py').read())" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: seed step failed - the database schema may now be incomplete:" -ForegroundColor Red
        Write-Host $seedOutput -ForegroundColor Red
        exit 1
    }
    Write-Host "Seed completed." -ForegroundColor Green
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
