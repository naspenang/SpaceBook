# This is accounts/views.py

from django.shortcuts import render

def account_home(request):
    return render(request, "accounts/home.html")

