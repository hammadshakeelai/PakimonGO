$ErrorActionPreference = "Continue"

$tools = @("git", "python", "pip", "flutter", "dart", "java", "adb", "gh")

foreach ($tool in $tools) {
    $cmd = Get-Command $tool -ErrorAction SilentlyContinue
    if ($cmd) {
        Write-Output "FOUND $tool => $($cmd.Source)"
    } else {
        Write-Output "MISSING $tool"
    }
}

Write-Output "ANDROID_HOME=$env:ANDROID_HOME"
Write-Output "ANDROID_SDK_ROOT=$env:ANDROID_SDK_ROOT"
Write-Output "JAVA_HOME=$env:JAVA_HOME"
Write-Output "FLUTTER_ROOT=$env:FLUTTER_ROOT"
Write-Output "PUB_CACHE=$env:PUB_CACHE"

if (Get-Command flutter -ErrorAction SilentlyContinue) {
    flutter --version
    flutter doctor -v
}

$defaultAdb = Join-Path $env:LOCALAPPDATA "Android\sdk\platform-tools\adb.exe"
if (Test-Path $defaultAdb) {
    Write-Output "FOUND adb SDK path => $defaultAdb"
    & $defaultAdb version
}
