import os
from PIL import Image

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Branch
from .forms import BranchForm


@login_required
def branch_create(request):
    if request.method == "POST":
        form = BranchForm(request.POST, request.FILES)
        if form.is_valid():
            branch = form.save()

            image = form.cleaned_data.get("image")
            if image:
                save_branch_image(branch.code, image)

            messages.success(request, "Branch added successfully.")
            return redirect("home")
    else:
        form = BranchForm()

    return render(
        request,
        "website/branch/branch_create.html",
        {"form": form},
    )


@login_required
def branch_edit(request, code):
    branch = get_object_or_404(Branch, code=code)

    if request.method == "POST":
        form = BranchForm(request.POST, request.FILES, instance=branch)
        if form.is_valid():
            branch = form.save()

            image = form.cleaned_data.get("image")
            if image:
                save_branch_image(branch.code, image)

            messages.success(request, "Branch updated successfully.")
            return redirect("home")
    else:
        form = BranchForm(instance=branch)

    return render(
        request,
        "website/branch/branch_update.html",
        {"form": form, "branch": branch},
    )


@login_required
def branch_delete(request, code):
    branch = get_object_or_404(Branch, code=code)

    if request.method == "POST":
        delete_branch_image(branch.code)
        branch.delete()

        messages.success(request, "Branch deleted successfully.")
        return redirect("home")

    return render(
        request,
        "website/branch/branch_delete.html",
        {"branch": branch},
    )


# -----------------------
# Helper functions
# -----------------------


def save_branch_image(branch_code, uploaded_file):
    filename = f"{branch_code.lower()}.jpg"
    folder = os.path.join(settings.MEDIA_ROOT, "branches")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    image = Image.open(uploaded_file)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.thumbnail((600, 400))
    image.save(path, "JPEG", quality=85, optimize=True)


def delete_branch_image(branch_code):
    filename = f"{branch_code.lower()}.jpg"
    path = os.path.join(settings.MEDIA_ROOT, "branches", filename)

    if os.path.isfile(path):
        os.remove(path)
