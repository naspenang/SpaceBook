# NOTE:
# This script WILL overwrite website/views.py and website/urls.py every time it runs.
# Only use it at the start of a project, not after you've customised those files.

# Django Init Script (venv + Django project + Home app)

Write-Host ""
Write-Host "=== Django Initial Setup ===" -ForegroundColor Cyan

# Get the current folder name to use as "project name" in the Home message
$projectName = Split-Path -Leaf (Get-Location).Path
Write-Host "Project name detected from folder: $projectName" -ForegroundColor Cyan


# -------------------------------------------------
# 1. Create virtual environment (.venv) if missing
# -------------------------------------------------
if (Test-Path ".\.venv") {
    Write-Host ""
    Write-Host "Virtual environment (.venv) already exists. Skipping creation." -ForegroundColor Yellow
}
else {
    Write-Host ""
    Write-Host "Creating virtual environment (.venv)..." -ForegroundColor Yellow
    py -3 -m venv .venv

    if (!(Test-Path ".\.venv")) {
        Write-Host "ERROR: Virtual environment was not created." -ForegroundColor Red
        exit 1
    }

    Write-Host "Virtual environment created." -ForegroundColor Green
}

# -------------------------------------------------
# 2. Activate virtual environment
# -------------------------------------------------
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

Write-Host "Virtual environment activated." -ForegroundColor Green
Write-Host "Python version in venv: " -NoNewline
python --version
Write-Host ""

# -------------------------------------------------
# 3. Upgrade pip
# -------------------------------------------------
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# -------------------------------------------------
# 4. Install Django + required packages
# -------------------------------------------------
Write-Host ""
Write-Host "Installing Django and required packages..." -ForegroundColor Yellow

python -m pip install "Django>=5,<6"
python -m pip install social-auth-app-django
python -m pip install django-environ
python -m pip install "django-htmx>=1,<2"

Write-Host "Package installation finished." -ForegroundColor Green

# -------------------------------------------------
# 5. Create Django project (${projectName}_project)
# -------------------------------------------------
if (Test-Path ".\manage.py") {
    Write-Host ""
    Write-Host "manage.py already exists. Skipping 'startproject'." -ForegroundColor Yellow
}
else {
    Write-Host ""
    Write-Host "Creating Django project: ${projectName}_project ..." -ForegroundColor Yellow
    django-admin startproject ${projectName}_project .

    if (!(Test-Path ".\manage.py")) {
        Write-Host "ERROR: manage.py not found. startproject may have failed." -ForegroundColor Red
        exit 1
    }

    Write-Host "Project created." -ForegroundColor Green
}

# Paths to key files
$settingsPath = ".\${projectName}_project\settings.py"
$urlsPath = ".\${projectName}_project\urls.py"

if (!(Test-Path $settingsPath) -or !(Test-Path $urlsPath)) {
    Write-Host "ERROR: Could not find ${projectName}_project/settings.py or urls.py" -ForegroundColor Red
    exit 1
}

# -------------------------------------------------
# 6. Create 'website' app
# -------------------------------------------------
if (Test-Path ".\website") {
    Write-Host ""
    Write-Host "App 'website' already exists. Skipping startapp." -ForegroundColor Yellow
}
else {
    Write-Host ""
    Write-Host "Creating Django app: website ..." -ForegroundColor Yellow
    python manage.py startapp website
    Write-Host "App 'website' created." -ForegroundColor Green
}

# -------------------------------------------------
# 7. Ensure 'website' is in INSTALLED_APPS
# -------------------------------------------------
Write-Host ""
Write-Host "Adding 'website' to INSTALLED_APPS (if missing)..." -ForegroundColor Yellow

$settingsLines = Get-Content $settingsPath

if ($settingsLines -notcontains '    "website",' -and $settingsLines -notcontains "    'website',") {

    $insertIndex = -1

    for ($i = 0; $i -lt $settingsLines.Length; $i++) {
        if ($settingsLines[$i] -match "django\.contrib\.staticfiles") {
            $insertIndex = $i + 1
            break
        }
    }

    if ($insertIndex -gt -1) {
        $before = $settingsLines[0..($insertIndex - 1)]
        $after = $settingsLines[$insertIndex..($settingsLines.Length - 1)]
        $newLine = '    "website",'
        $settingsLines = $before + $newLine + $after
        $settingsLines | Set-Content $settingsPath -Encoding utf8
        Write-Host "'website' added to INSTALLED_APPS." -ForegroundColor Green
    }
    else {
        Write-Host "WARNING: Could not automatically insert 'website' into INSTALLED_APPS. Please add it manually." -ForegroundColor Yellow
    }
}
else {
    Write-Host "'website' already present in INSTALLED_APPS." -ForegroundColor Yellow
}

# -------------------------------------------------
# 8. Ensure APP_DIRS = True in TEMPLATES
# -------------------------------------------------
Write-Host ""
Write-Host "Ensuring APP_DIRS = True in TEMPLATES setting..." -ForegroundColor Yellow

$settingsText = Get-Content $settingsPath -Raw

if ($settingsText -notmatch "APP_DIRS\s*=\s*True") {
    $settingsText = $settingsText -replace "APP_DIRS\s*=\s*False", "APP_DIRS = True"
    if ($settingsText -notmatch "APP_DIRS\s*=\s*True") {
        # If APP_DIRS was missing completely, try to inject it
        $settingsText = $settingsText -replace "'DIRS': \[\],", "'DIRS': [],`r`n        'APP_DIRS': True,"
    }
    $settingsText | Set-Content $settingsPath -Encoding utf8
    Write-Host "APP_DIRS set to True." -ForegroundColor Green
}
else {
    Write-Host "APP_DIRS already set to True." -ForegroundColor Yellow
}

# -------------------------------------------------
# 9. Create website/views.py with dynamic message
# -------------------------------------------------
Write-Host ""
Write-Host "Creating website/views.py with template-based home view..." -ForegroundColor Yellow

@"
from django.shortcuts import render


def home(request):
    return render(request, "website/home.html")
"@ | Set-Content ".\website\views.py" -Encoding utf8

Write-Host "website/views.py created." -ForegroundColor Green

# -------------------------------------------------
# 10. Create website/urls.py
# -------------------------------------------------
Write-Host ""
Write-Host "Creating website/urls.py ..." -ForegroundColor Yellow

@"
from django.urls import path
from .views import home

urlpatterns = [
    path("", home, name="home"),
]
"@ | Set-Content ".\website\urls.py" -Encoding utf8

Write-Host "website/urls.py created." -ForegroundColor Green


# -------------------------------------------------
# 11 Create templates for website: base, nav, home, footer
# -------------------------------------------------
Write-Host ""
Write-Host "Creating templates for 'website' (base.html, nav.html, home.html, footer.html)..." -ForegroundColor Yellow

$templatesDir = ".\website\templates\website"
if (-not (Test-Path $templatesDir)) {
    New-Item -ItemType Directory -Path $templatesDir | Out-Null
}

$basePath = Join-Path $templatesDir "base.html"
$navPath = Join-Path $templatesDir "nav.html"
$homePath = Join-Path $templatesDir "home.html"
$footerPath = Join-Path $templatesDir "footer.html"

if (-not (Test-Path $navPath)) {
    @"
<nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
  <div class="container-fluid">
    <a class="navbar-brand" href="/">
      <img src="/media/logo.png" style="height: 40px; margin-top: -5px" />
      $projectName
    </a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNav">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="mainNav">
      <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
        <!-- AUTO-GENERATED NAV START -->
        <!-- AUTO-GENERATED NAV END -->
      </ul>
    </div>
  </div>
</nav>
"@ | Set-Content $navPath -Encoding utf8
    Write-Host "Created website/nav.html" -ForegroundColor Green
}
else {
    Write-Host "website/nav.html already exists, skipping." -ForegroundColor Yellow
}

if (-not (Test-Path $footerPath)) {
    @"
<footer class="bg-dark text-white text-center py-3 mt-5">
  <div class="container">
    <small>&copy; 2025 Your Project Name. All rights reserved.</small>
  </div>
</footer>
"@ | Set-Content $footerPath -Encoding utf8
    Write-Host "Created website/footer.html" -ForegroundColor Green
}
else {
    Write-Host "website/footer.html already exists, skipping." -ForegroundColor Yellow
}

if (-not (Test-Path $basePath)) {
    @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}Website{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    {% include "website/nav.html" %}
    <div class="container my-4">
        {% block content %}{% endblock %}
    </div>
    {% include "website/footer.html" %}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"@ | Set-Content $basePath -Encoding utf8
    Write-Host "Created website/base.html" -ForegroundColor Green
}
else {
    Write-Host "website/base.html already exists, skipping." -ForegroundColor Yellow
}

if (-not (Test-Path $homePath)) {
    @"
{% extends "website/base.html" %}

{% block title %}Home | Website{% endblock %}

{% block content %}
<div class="text-center my-5">
    <h1>Website for the $projectName successfully running</h1>
    <p>This home page was generated by _project_init.ps1.</p>
</div>
{% endblock %}
"@ | Set-Content $homePath -Encoding utf8
    Write-Host "Created website/home.html" -ForegroundColor Green
}
else {
    Write-Host "website/home.html already exists, skipping." -ForegroundColor Yellow
}



# -------------------------------------------------
# 11.1 + 11.2 Create VS Code .vscode/launch.json and tasks.json
# -------------------------------------------------
Write-Host ""
Write-Host "Creating VS Code .vscode/launch.json and tasks.json ..." -ForegroundColor Yellow

# Make sure .vscode folder exists
$vscodeDir = ".\.vscode"
if (-not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}

# Figure out settings module, based on the folder name
$settingsModule = "${projectName}_project.settings"

# Get absolute path to venv python, e.g. d:\DJANGO-PROJECTS\SeparaBooks\.venv\Scripts\python.exe
$projectRoot = Get-Location
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "WARNING: .venv\\Scripts\\python.exe not found. launch.json will still use 'python'." -ForegroundColor Yellow
    $venvPython = "python"
}
else {
    Write-Host "Using venv python at: $venvPython" -ForegroundColor Green
}


# ---------- launch.json (matches your template) ----------
$launchJson = @"
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "python",
            "request": "launch",
            "program": "`${workspaceFolder}/manage.py",
            "console": "integratedTerminal",
            "django": true,
            "env": {
                "DJANGO_SETTINGS_MODULE": "$settingsModule"
            },
            "python": "`${workspaceFolder}/.venv/Scripts/python.exe",
            "name": "Django: Runserver (Debug)",
            "args": [
                "runserver",
                "8000"
            ],
            "justMyCode": false,
            "serverReadyAction": {
                "action": "openExternally",
                "pattern": "Starting development server at (http://127\\.0\\.0\\.1:8000/?)",
                "uriFormat": "%s"
            }
        },
        {
            "type": "python",
            "request": "launch",
            "program": "`${workspaceFolder}/manage.py",
            "console": "integratedTerminal",
            "django": true,
            "env": {
                "DJANGO_SETTINGS_MODULE": "$settingsModule"
            },
            "python": "`${workspaceFolder}/.venv/Scripts/python.exe",
            "name": "Django: Runserver (No Debug)",
            "args": [
                "runserver",
                "8000",
                "--noreload"
            ],
            "justMyCode": true,
            "serverReadyAction": {
                "action": "openExternally",
                "pattern": "Starting development server at (http://127\\.0\\.0\\.1:8000/?)",
                "uriFormat": "%s"
            }
        },
        {
            "type": "python",
            "request": "launch",
            "program": "`${workspaceFolder}/manage.py",
            "console": "integratedTerminal",
            "django": true,
            "env": {
                "DJANGO_SETTINGS_MODULE": "$settingsModule"
            },
            "python": "`${workspaceFolder}/.venv/Scripts/python.exe",
            "name": "Django: Tests",
            "args": [
                "test"
            ],
            "justMyCode": true
        },
        {
            "type": "python",
            "request": "launch",
            "program": "`${workspaceFolder}/manage.py",
            "console": "integratedTerminal",
            "django": true,
            "env": {
                "DJANGO_SETTINGS_MODULE": "$settingsModule"
            },
            "python": "`${workspaceFolder}/.venv/Scripts/python.exe",
            "name": "Django: Shell",
            "args": [
                "shell"
            ],
            "justMyCode": true
        }
    ]
}
"@

$launchFile = Join-Path $vscodeDir "launch.json"
$launchJson | Set-Content $launchFile -Encoding utf8
Write-Host "VS Code launch.json created at $launchFile" -ForegroundColor Green
Write-Host "DJANGO_SETTINGS_MODULE = $settingsModule" -ForegroundColor Cyan

# ---------- tasks.json ----------
$tasksData = @{
    version = "2.0.0"
    tasks   = @(
        @{
            label          = "Django: Runserver"
            type           = "shell"
            command        = $venvPython
            args           = @("manage.py", "runserver")
            group          = @{
                kind      = "build"
                isDefault = $true
            }
            problemMatcher = @()
        },
        @{
            label          = "Django: Make Migrations"
            type           = "shell"
            command        = $venvPython
            args           = @("manage.py", "makemigrations")
            group          = "none"
            problemMatcher = @()
        },
        @{
            label          = "Django: Run Migrations"
            type           = "shell"
            command        = $venvPython
            args           = @("manage.py", "migrate")
            group          = "none"
            problemMatcher = @()
        }
    )
}

$tasksJson = $tasksData | ConvertTo-Json -Depth 10
$tasksFile = Join-Path $vscodeDir "tasks.json"
$tasksJson | Set-Content $tasksFile -Encoding utf8

Write-Host "VS Code tasks.json created at $tasksFile"   -ForegroundColor Green


# -------------------------------------------------
# 11.7 VS Code: auto-activate .venv using Python extension (Method 2)
# -------------------------------------------------
Write-Host ""
Write-Host "Configuring VS Code to auto-activate .venv (Python extension)..." -ForegroundColor Yellow

if (-not (Test-Path $vscodeDir)) {
    New-Item -ItemType Directory -Path $vscodeDir | Out-Null
}

$settingsFile = Join-Path $vscodeDir "settings.json"

# This will overwrite settings.json with the Python-related settings.
# If you ever want to keep extra custom settings, we can change this later to merge instead.
$settingsData = @{
    "python.terminal.activateEnvironment" = $true
    "python.defaultInterpreterPath"       = ".venv\\Scripts\\python.exe"
}

$settingsJson = $settingsData | ConvertTo-Json -Depth 5
$settingsJson | Set-Content $settingsFile -Encoding utf8

Write-Host "✅ VS Code settings.json written for auto-venv:" -ForegroundColor Green
Write-Host "   - python.terminal.activateEnvironment = true" -ForegroundColor Green
Write-Host "   - python.defaultInterpreterPath = .venv\\Scripts\\python.exe" -ForegroundColor Green


# -------------------------------------------------
# 11.8 Update project urls.py to point root URL ('/') to website app
# -------------------------------------------------
Write-Host ""
Write-Host "Updating project urls.py to point root URL ('/') to website app..." -ForegroundColor Yellow

$urlsLines = Get-Content $urlsPath

# Ensure "include" is imported
for ($i = 0; $i -lt $urlsLines.Length; $i++) {
    if ($urlsLines[$i] -match "from django\.urls import path" -and $urlsLines[$i] -notmatch "include") {
        $urlsLines[$i] = "from django.urls import path, include"
        break
    }
}

# Insert path("", include("website.urls")), if not present
$hasWebsiteRoute = $false
foreach ($line in $urlsLines) {
    if ($line -match "website\.urls") {
        $hasWebsiteRoute = $true
        break
    }
}

if (-not $hasWebsiteRoute) {
    $insertIndex = -1
    for ($i = 0; $i -lt $urlsLines.Length; $i++) {
        if ($urlsLines[$i] -match "admin\.site\.urls") {
            $insertIndex = $i + 1
            break
        }
    }

    if ($insertIndex -gt -1) {
        $before = $urlsLines[0..($insertIndex - 1)]
        $after = $urlsLines[$insertIndex..($urlsLines.Length - 1)]
        $newLine = '    path("", include("website.urls")),'
        
        $urlsLines = $before + $newLine + $after
        $urlsLines | Set-Content $urlsPath -Encoding utf8
        Write-Host 'Root URL now points to website app.' -ForegroundColor Green
    }
    else {
        Write-Host "WARNING: Could not automatically insert website route in urls.py. Please add it manually." -ForegroundColor Yellow
    }
}
else {
    Write-Host "website route already exists in urls.py." -ForegroundColor Yellow
}


# -------------------------------------------------
# 11.9 Copy _setup.py to every app folder
# -------------------------------------------------
# Path to the file you want to copy
$sourceFile = "_setup.blank"

# Make sure the source exists
if (-not (Test-Path $sourceFile)) {
    Write-Host "Source file '$sourceFile' not found."
    return
}

# Find every folder that contains apps.py
$targets = Get-ChildItem -Recurse -Filter "apps.py"

foreach ($t in $targets) {
    $targetFolder = $t.Directory.FullName
    $destPath = Join-Path $targetFolder "_setup.py"

    Copy-Item -Path $sourceFile -Destination $destPath -Force
    Write-Host "Copied to: $destPath"
}


# -------------------------------------------------
# 12. Done
# -------------------------------------------------
Write-Host ""
Write-Host "=== $projectName Django base setup + Website app completed ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now you can run:" -ForegroundColor Cyan
Write-Host "    python manage.py runserver" -ForegroundColor Cyan
Write-Host ""
Write-Host "Then open http://127.0.0.1:8000/ and you should see:" -ForegroundColor Cyan
Write-Host "    Website for the $projectName successfully running" -ForegroundColor Green
