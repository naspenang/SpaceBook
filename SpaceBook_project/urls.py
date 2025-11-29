from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # include all urls from the website app (home + profile)
    path("", include("website.urls")),
    # auth + social
    path("accounts/", include("django.contrib.auth.urls")),
    path("oauth/", include("social_django.urls", namespace="social")),
]
