
# Deployment Guide  
## Django + Uvicorn Behind IIS on Windows Server 2019

This is a full, step‑by‑step guide you can reuse on any new Windows Server 2019 machine to host a Django app behind IIS using Uvicorn.

The examples use:

- **Server OS**: Windows Server 2019 Datacenter  
- **Python**: 3.13.x (64‑bit)  
- **Django project root**: `D:\django_projects\spacebook`  
- **Virtual environment**: `D:\django_env`  
- **IIS Site**: `Default Web Site`  
- **IIS app path**: `/spacebook`  
- **Uvicorn bind**: `127.0.0.1:8000`

You can swap names/paths/ports, but keep the structure.

---

## 1. Prepare IIS

### 1.1 Open IIS Manager

1. Press **Start**.
2. Search for **Internet Information Services (IIS) Manager**.
3. Open it.

### 1.2 Check the main site and bindings

1. In the **Connections** panel on the left:
   - Expand your server name.
   - Click **Sites**.
   - Click **Default Web Site** (or whatever main site you use).

2. In the **Actions** panel on the right, click **Bindings…**.

You should see at least:

- Type: `http`, Port: `80`, IP address: `*`
- Type: `https`, Port: `443`, IP address: `*` (if you already use SSL)

> If you don’t have port 80 set up, make one now before continuing.

### 1.3 Make sure URL Rewrite + ARR are installed

Under the server node (top of tree, *not* the site):

1. Click the **server name** in the left panel.
2. In middle panel, look for these icons:
   - **URL Rewrite**
   - **Application Request Routing Cache**

If either is missing:

- Install them via **Web Platform Installer** or download from Microsoft.  
- After install, restart IIS Manager.

These two bits are what let IIS act as a reverse proxy.

---

## 2. Install / Check Python and Virtual Environment

### 2.1 Check Python

Open **Command Prompt** (Win + R → `cmd` → Enter) and run:

```cmd
python --version
py --list
```

You should see something like:

```text
Python 3.13.9
 -V:3.13 *   Python 3.13 (64-bit)
```

If Python isn’t installed:

1. Install **64‑bit** Python for Windows.
2. Tick **“Add python.exe to PATH”** in the installer.
3. Re‑open CMD and run the commands again.

### 2.2 Create or reuse a virtual environment

If you’re setting up from scratch:

```cmd
python -m venv D:\django_env
```

To activate it:

```cmd
D:\django_env\Scripts\activate
```

Your prompt should change to:

```text
(django_env) C:\Users\Administrator>
```

> Always activate this venv before installing packages or running Django/Uvicorn.

---

## 3. Place Your Django Project

On the server, decide a folder for Django projects, e.g.:

```text
D:\django_projects\
```

Inside that, put your project folder, e.g.:

```text
D:\django_projects\spacebook\
```

Typical structure:

```text
spacebook\
  manage.py
  db.sqlite3 (or none if using external DB)
  staticfiles\
  logs\
  spacebook_project\    # Django project module
    __init__.py
    settings.py
    urls.py
    asgi.py
    wsgi.py
  ...other app folders...
```

The important part:  
The folder that contains `asgi.py` is the module you’ll pass to Uvicorn, for example:

```text
spacebook_project.asgi:application
```

---

## 4. Install Django, Uvicorn, and psutil in the venv

With the venv **activated**:

```cmd
pip install "django" "uvicorn[standard]" psutil
```

(If Django is already installed you’ll just see it skipped or updated.)

You can confirm:

```cmd
python -m django --version
uvicorn --version
```

---

## 5. Run Uvicorn Manually (First Test)

Still in the activated venv:

```cmd
cd D:\django_projects\spacebook
uvicorn spacebook_project.asgi:application --host 127.0.0.1 --port 8000
```

You should see something like:

```text
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

While that’s running, open a browser **on the server**:

- Go to `http://127.0.0.1:8000/`

If your Django project is set up right, your site’s home page should appear.  
You might see missing CSS/images for now — we’ll fix static files later.

Press **Ctrl + C** in the CMD window to stop Uvicorn after testing.

---

## 6. Create the IIS Application for the Django Site

We’ll host the site as `/spacebook` under **Default Web Site**.

### 6.1 Add the IIS application

1. In IIS Manager, expand:
   - **Sites → Default Web Site**
2. Right‑click **Default Web Site → Add Application…**

Fill in:

- **Alias**: `spacebook`
- **Application pool**: choose an existing pool (e.g. `DefaultAppPool` or one you use for internal apps).
- **Physical path**:  
  `D:\django_projects\spacebook`

Click **OK**.

Now you should see a **spacebook** node under Default Web Site.

---

## 7. Create the Reverse Proxy Rule in URL Rewrite

We want IIS to forward any URL under `/spacebook/` to Uvicorn on `127.0.0.1:8000`.

### 7.1 Open URL Rewrite for this app

1. In IIS left panel, click **spacebook** under **Default Web Site**.
2. In the middle, double‑click **URL Rewrite**.

### 7.2 Add the inbound rule

If you already have a rule from a previous setup, you can just edit it.  
To create a new one:

1. In the right panel, click **Add Rule(s)…**
2. Choose **“Blank rule”** under *Inbound rules*.
3. Click **OK**.

Fill the rule like this:

**Name:**  
`ProxyToDjango`

**Match URL:**

- Requested URL: **Matches the Pattern**
- Using: **Regular Expressions**
- Pattern:

  ```text
  (.*)
  ```

(or if you want more strict, you can use `^(.*)` — both are fine here inside the app)

**Conditions:**

- Add a condition:
  - Condition input: `{REQUEST_FILENAME}`
  - Check if input string: **Is Not a File**

(This keeps real files served directly if present.)

**Action:**

- Action type: **Rewrite**
- Rewrite URL:

  ```text
  http://127.0.0.1:8000/{R:1}
  ```

- Check **Append query string**
- Check **Stop processing of subsequent rules**

Click **Apply** on the right.

---

## 8. Serve Static Files via IIS

Django should not serve static files in production; IIS is better at it.

Assume your collected static files live here:

```text
D:\django_projects\spacebook\staticfiles\
```

If you don’t have that yet, set these in `settings.py` and run `collectstatic` later:

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
```

Then:

```cmd
python manage.py collectstatic
```

### 8.1 Create the `/static` virtual directory

1. In IIS, under **Default Web Site → spacebook**, right‑click **spacebook**.
2. Click **Add Virtual Directory…**.

Fill in:

- Alias: `static`
- Physical path: `D:\django_projects\spacebook\staticfiles`

Click **OK**.

### 8.2 Convert `/static` to an application

1. Right‑click the new **static** entry.
2. Click **Convert to Application…**
3. Use the same application pool as the main app (or DefaultAppPool).
4. Click **OK**.

Now URLs like:

```text
http://localhost/spacebook/static/...
```

will come straight from the disk, not Uvicorn.

---

## 9. Test IIS → Uvicorn Manually

1. Start Uvicorn manually again:

```cmd
D:\django_env\Scripts\activate
cd D:\django_projects\spacebook
uvicorn spacebook_project.asgi:application --host 127.0.0.1 --port 8000
```

2. In a browser on the server:

- Go to: `http://localhost/spacebook/`

If it loads and static files work (`/spacebook/static/...`), your basic proxy chain is correct.

Press **Ctrl + C** to stop Uvicorn once done.

---

## 10. Install and Check NSSM

NSSM (Non‑Sucking Service Manager) runs Uvicorn as a Windows service.

If NSSM is already installed:

```cmd
nssm
```

You should see help text like “The non‑sucking service manager”.

If not, download NSSM, put `nssm.exe` somewhere on `PATH` (or in `C:\Windows\System32`), and run the command again.

---

## 11. Create the Uvicorn Windows Service

We’ll make a service called `spacebook-uvicorn` that runs Uvicorn in your venv.

Open **Command Prompt as Administrator** and run:

```cmd
nssm install spacebook-uvicorn
```

A small GUI will appear.

### 11.1 Application tab

Set:

- **Path:**

  ```text
  D:\django_env\Scripts\python.exe
  ```

- **Startup directory:**

  ```text
  D:\django_projects\spacebook
  ```

- **Arguments:** (this is important; no space between `-` and `m`)

  ```text
  -m uvicorn spacebook_project.asgi:application --host 127.0.0.1 --port 8000 --lifespan off --loop asyncio --http auto --timeout-keep-alive 30 --proxy-headers --forwarded-allow-ips="*"
  ```

Click **Install service**.

### 11.2 Details tab (optional niceness)

- Display name: `SpaceBook Uvicorn Server`
- Startup type: `Automatic`

Save.

---

## 12. Configure Restart on Crash (NSSM)

To make sure Uvicorn restarts if it crashes:

```cmd
nssm edit spacebook-uvicorn
```

Go to the **Exit actions** (or **Shutdown / Exit** depending on version) tab.

Make sure it says something like:

- `Action to take when application exits: Restart application`
- “Delay restart if application runs for less than 1500 ms” can stay at default.

Click **Edit service** to save.

---

## 13. Start the Service and Test

Start the service:

```cmd
nssm start spacebook-uvicorn
```

Or use `services.msc` → find **SpaceBook Uvicorn Server** → Start.

Now:

1. Test direct Uvicorn:

   ```text
   http://127.0.0.1:8000/
   ```

2. Test through IIS:

   ```text
   http://localhost/spacebook/
   http://SERVERNAME/spacebook/
   ```

If both work, Uvicorn is correctly running as a service and IIS is proxying.

---

## 14. Add a Health Check Endpoint in Django

You want a URL that says if the app, DB, cache and server look healthy.

### 14.1 Install `psutil` (if not done earlier)

In venv:

```cmd
pip install psutil
```

### 14.2 Add health view and route

Open your main project `urls.py`, e.g.:

```text
D:\django_projects\spacebook\spacebook_project\urls.py
```

At the top of the file add:

```python
import socket
import sys
import platform
import psutil

from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache
from django.utils import timezone
import django
```

Somewhere near the top:

```python
STARTED_AT = timezone.now()
```

Then add the health view:

```python
def health(request):
    # Database check
    db_ok = False
    db_error = None
    try:
        conn = connections["default"]
        conn.cursor().execute("SELECT 1")
        db_ok = True
    except OperationalError as e:
        db_error = str(e)

    # Cache check
    cache_ok = False
    cache_error = None
    try:
        cache.set("__hc__", "ok", 5)
        cache_ok = cache.get("__hc__") == "ok"
    except Exception as e:
        cache_error = str(e)

    # System metrics
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("D:\\")

    # Uvicorn process info
    proc = psutil.Process()
    proc_mem = proc.memory_info().rss

    overall_ok = db_ok and cache_ok

    data = {
        "status": "ok" if overall_ok else "degraded",
        "app": "spacebook",
        "host": socket.gethostname(),
        "time": timezone.now().isoformat(),
        "started_at": STARTED_AT.isoformat(),
        "checks": {
            "database": {"ok": db_ok, "error": db_error},
            "cache": {"ok": cache_ok, "error": cache_error},
        },
        "system": {
            "cpu_percent": cpu_percent,
            "memory": {
                "total": mem.total,
                "used": mem.used,
                "percent": mem.percent,
            },
            "disk_D": {
                "total": disk.total,
                "used": disk.used,
                "percent": disk.percent,
            },
        },
        "process": {
            "pid": proc.pid,
            "memory_bytes": proc_mem,
            "uptime_seconds": (timezone.now() - STARTED_AT).total_seconds(),
        },
        "versions": {
            "python": sys.version.split()[0],
            "django": django.get_version(),
            "platform": platform.platform(),
        },
    }

    return JsonResponse(data, status=200 if overall_ok else 503)
```

Finally, wire up the URL path:

```python
from django.urls import path

urlpatterns = [
    # ... your other routes ...
    path("health/", health, name="health"),
]
```

Restart the service:

```cmd
nssm restart spacebook-uvicorn
```

Test:

```text
http://localhost/spacebook/health/
```

You should get a JSON output containing:

- `status`
- `checks.database`
- `checks.cache`
- `system`
- `process`
- `versions`

You can hook this URL into:
- UptimeRobot
- Zabbix/Nagios/PRTG
- Any monitoring/check script

Treat `"status": "ok"` as healthy; `"degraded"` or HTTP `503` as bad.

---

## 15. Quick Checklist for New Servers

When you set up a new server, you can roughly follow this checklist:

1. Install **IIS**, **URL Rewrite**, **ARR**.
2. Confirm **Default Web Site** bindings on ports 80/443.
3. Install **Python 64‑bit**, create `D:\django_env`.
4. Put Django project under `D:\django_projects\PROJECTNAME`.
5. Activate venv, `pip install django uvicorn[standard] psutil`.
6. Make sure `PROJECTNAME_project.asgi:application` works with Uvicorn on port 8000.
7. Create IIS **Application** `/projectname` pointing at the folder.
8. Add **URL Rewrite** rule to proxy to `http://127.0.0.1:8000/{R:1}`.
9. Configure static files:
   - `STATIC_ROOT = BASE_DIR / "staticfiles"`
   - run `collectstatic`
   - IIS virtual directory `/static` → `staticfiles` (convert to app).
10. Install **NSSM**, create `projectname-uvicorn` service:
    - Path: venv `python.exe`
    - Startup directory: project folder
    - Arguments: `-m uvicorn ...` with flags above.
11. Set service to **Automatic** and **Restart application** on exit.
12. Add `/health/` endpoint and confirm it returns `"status": "ok"`.

If all boxes are ticked, you’re good to go.

---

That’s the full deployment recipe. You can copy this whole `.md` file to any new server or print it as a reference.
