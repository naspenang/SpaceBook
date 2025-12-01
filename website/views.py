# this is website/views.py

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Branch
from .forms import BranchForm


# Create your views here.


def home(request):
    branches = Branch.objects.all().order_by("name")  # router sends this to main.db
    return render(request, "website/home.html", {"branches": branches})


@login_required
def profile(request):
    return render(request, "website/profile.html")


def about(request):
    return render(request, "website/about.html")


@login_required
def branch_create(request):
    """
    Create a new Branch record in main.db.
    Only logged-in users can access this.
    """
    if request.method == "POST":
        form = BranchForm(request.POST, request.FILES)  # ← add request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Branch added successfully.")
            return redirect("home")
    else:
        form = BranchForm()

    return render(request, "website/branch_form.html", {"form": form})


def blank(request):
    greeting = ""  # default value

    if request.method == "POST":
        fullname = request.POST.get("fullname", "")
        greeting = f"Hello, {fullname}!"

    context = {"greeting": greeting}

    return render(request, "website/_blank.html", context)
