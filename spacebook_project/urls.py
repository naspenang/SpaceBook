# this is the main urls.py file for the project

import socket
import sys
import platform
import psutil
import django

from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from django.core.cache import cache
from django.utils import timezone


STARTED_AT = timezone.now()


def health(request):
    # ---- DB check ----
    db_ok = False
    db_error = None
    try:
        conn = connections["default"]
        conn.cursor().execute("SELECT 1")
        db_ok = True
    except OperationalError as e:
        db_error = str(e)

    # ---- Cache check ----
    cache_ok = False
    cache_error = None
    try:
        cache.set("__healthcheck__", "ok", 5)
        cache_ok = cache.get("__healthcheck__") == "ok"
    except Exception as e:  # noqa: BLE001
        cache_error = str(e)

    # ---- System stats (psutil) ----
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("D:\\")

    # ---- Process info ----
    proc = psutil.Process()
    proc_mem = proc.memory_info().rss  # bytes

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


urlpatterns = [
    path("", lambda request: redirect("/spacebook/")),  # 👈 root redirect
    path("spacebook/admin/", admin.site.urls),
    path(
        "spacebook/", include("website.urls")
    ),  # include all urls from the website app (home + profile)
    path("spacebook/accounts/", include("django.contrib.auth.urls")),  # auth + social
    path("spacebook/oauth/", include("social_django.urls", namespace="social")),
    path("spacebook/health/", health, name="health"),
]
