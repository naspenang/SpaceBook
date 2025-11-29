# this is website/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Branch

# Create your views here.


def home(request):
    branches = Branch.objects.all().order_by("name")  # router sends this to main.db
    return render(request, "website/home.html", {"branches": branches})


@login_required
def profile(request):
    return render(request, "website/profile.html")

