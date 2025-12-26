from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Branch


def home(request):
    branches = Branch.objects.all().order_by("name")
    return render(request, "website/home.html", {"branches": branches})


@login_required
def profile(request):
    return render(request, "website/profile.html")


def about(request):
    return render(request, "website/about.html")


def blank(request):
    greeting = ""
    if request.method == "POST":
        greeting = f"Hello, {request.POST.get('fullname', '')}"
    return render(request, "website/_blank.html", {"greeting": greeting})
