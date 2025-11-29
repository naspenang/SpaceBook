# This is website/urls.py

from django.urls import path
from . import views
from .views import home, profile, branch_create

urlpatterns = [
    path("", home, name="home"),
    path("profile/", profile, name="profile"),
    path("about/", views.about, name="about"),
    path("branches/add/", branch_create, name="branch_add"),
]
