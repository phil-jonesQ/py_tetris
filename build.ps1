$ErrorActionPreference = "Stop"
$appName = "py_tetris"
$distDirectory = Join-Path $PSScriptRoot "dist"
$appDirectory = Join-Path $distDirectory $appName
$archivePath = Join-Path $distDirectory "$appName.zip"
$workDirectory = Join-Path $PSScriptRoot "build\pyinstaller"
$buildEnvironment = Join-Path ([System.IO.Path]::GetTempPath()) "py-tetris-build-$([guid]::NewGuid().ToString('N'))"
$uvCommand = Get-Command uv -ErrorAction SilentlyContinue

if (-not $uvCommand) {
    python.exe -m uv --version
    if ($LASTEXITCODE -ne 0) {
        throw "uv is required. Install it from https://docs.astral.sh/uv/getting-started/installation/"
    }
}

function Invoke-Uv {
    param([string[]]$UvArguments)

    if ($uvCommand) {
        & $uvCommand.Source @UvArguments
    }
    else {
        python.exe -m uv @UvArguments
    }
    if ($LASTEXITCODE -ne 0) {
        throw "uv $($UvArguments -join ' ') failed with exit code $LASTEXITCODE"
    }
}

Push-Location $PSScriptRoot
$previousProjectEnvironment = $env:UV_PROJECT_ENVIRONMENT
try {
    $env:UV_PROJECT_ENVIRONMENT = $buildEnvironment
    Invoke-Uv -UvArguments @("sync", "--locked", "--extra", "dev", "--link-mode", "copy")
    Invoke-Uv -UvArguments @("run", "pytest")

    if (Test-Path -LiteralPath $appDirectory) {
        Remove-Item -LiteralPath $appDirectory -Recurse -Force
    }
    if (Test-Path -LiteralPath $archivePath) {
        Remove-Item -LiteralPath $archivePath -Force
    }
    if (Test-Path -LiteralPath $workDirectory) {
        Remove-Item -LiteralPath $workDirectory -Recurse -Force
    }
    New-Item -ItemType Directory -Path $appDirectory, $workDirectory -Force | Out-Null

    Invoke-Uv -UvArguments @(
        "run", "pyinstaller", "--noconfirm", "--clean", "--onefile",
        "--name", $appName,
        "--distpath", $appDirectory,
        "--workpath", $workDirectory,
        "--specpath", $workDirectory,
        ".\py_tetris.py"
    )

    Copy-Item -LiteralPath (Join-Path $PSScriptRoot "game_assets") -Destination $appDirectory -Recurse
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot "high_score.json") -Destination $appDirectory
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot "README.md") -Destination $appDirectory
    Compress-Archive -Path (Join-Path $appDirectory "*") -DestinationPath $archivePath

    Write-Output "Build complete: $appDirectory"
    Write-Output "Archive created: $archivePath"
}
finally {
    if ($null -eq $previousProjectEnvironment) {
        Remove-Item Env:UV_PROJECT_ENVIRONMENT -ErrorAction SilentlyContinue
    }
    else {
        $env:UV_PROJECT_ENVIRONMENT = $previousProjectEnvironment
    }
    Pop-Location
    if (Test-Path -LiteralPath $buildEnvironment) {
        Remove-Item -LiteralPath $buildEnvironment -Recurse -Force
    }
}
