from django.urls import path
from .views import account_home

urlpatterns = [
    path("", account_home, name="account_home"),
]
