# ===============================
# SpaceBook Project Zipper
# (Structure-safe version)
# ===============================

$ErrorActionPreference = "Stop"

$rootPath = Get-Location
$zipName  = "spacebook.zip"
$zipPath  = Join-Path $rootPath $zipName
$tempDir  = Join-Path $rootPath "__zip_temp__"

# Folder names to exclude (any depth)
$excludeFolders = @(
    ".git",
    "__pycache__",
    "migrations",
    "static",
    "staticfiles",
    "media",
    "src",
    "venv",
    "env",
    ".venv",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
    "__zip_temp__"
)

# File patterns to exclude
$excludeFiles = @(
    "*.log",
    "*.db",
    "*.sqlite3",
    "*.zip",
    "*.ps1",
    "*.md",
    "*.bat",
    ".DS_Store",
    "Thumbs.db",
    ".gitignore",
    "web.config",
    "LICENSE"
)

# -------------------------------
# Cleanup old ZIP and temp folder
# -------------------------------
if (Test-Path $zipPath) {
    try {
        Remove-Item $zipPath -Force
    }
    catch {
        Write-Error "Failed to delete existing $zipName."
        exit 1
    }
}

if (Test-Path $tempDir) {
    Remove-Item $tempDir -Recurse -Force
}

New-Item -ItemType Directory -Path $tempDir | Out-Null

# -------------------------------
# Copy files while preserving structure
# -------------------------------
Get-ChildItem -Path $rootPath -Recurse -File -Force | ForEach-Object {

    # Exclude by folder name
    foreach ($folder in $excludeFolders) {
        if ($_.FullName -split '[\\/]' -contains $folder) {
            return
        }
    }

    # Exclude by file pattern / filename
    foreach ($pattern in $excludeFiles) {
        if ($_.Name -like $pattern) {
            return
        }
    }

    # Build relative path
    $relativePath = $_.FullName.Substring($rootPath.Path.Length).TrimStart('\','/')
    $targetPath  = Join-Path $tempDir $relativePath
    $targetDir   = Split-Path $targetPath -Parent

    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }

    Copy-Item $_.FullName -Destination $targetPath -Force
}

# -------------------------------
# Create ZIP from temp directory
# -------------------------------
Compress-Archive -Path (Join-Path $tempDir '*') -DestinationPath $zipPath

# -------------------------------
# Cleanup temp directory
# -------------------------------
Remove-Item $tempDir -Recurse -Force

Write-Host "spacebook.zip created successfully with folder structure preserved."
