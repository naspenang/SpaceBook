# this is the main urls.py file for the project

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("website.urls")), # include all urls from the website app (home + profile)
    path("accounts/", include("django.contrib.auth.urls")), # auth + social
    path("oauth/", include("social_django.urls", namespace="social")), 
]
