import os
from django.http import JsonResponse
from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Branch
from ..forms import BranchForm


# -----------------------
#  Pages Code
# -----------------------
from website.models import Campus

def branch_detail(request, code):
    branch = get_object_or_404(Branch, code=code)

    campuses = Campus.objects.filter(
        branch=branch
    ).order_by("campus_name")

    return render(request, "website/branch/branch_detail.html", {
        "branch": branch,
        "campuses": campuses
    })



def branch_list(request):
    query = request.GET.get("q", "")

    branches = Branch.objects.filter(
        name__icontains=query
    ).order_by("name")

    view_mode = request.GET.get("view", "grid")

    return render(
        request,
        "website/branch/branch_list.html",
        {
            "branches": branches,
            "view_mode": view_mode,
            "query": query,
        },
    )



def branch_list_embed(request):
    query = request.GET.get("q", "")

    branches = Branch.objects.filter(
        name__icontains=query
    ).order_by("name")

    view_mode = request.GET.get("view", "grid")

    return render(
        request,
        "website/branch/branch_list_embed.html",
        {
            "branches": branches,
            "view_mode": view_mode,
            "query": query,
        },
    )




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
#  API
# -----------------------


def branch_list_api(request):
    branches = Branch.objects.all().order_by("name")

    data = []
    for b in branches:
        data.append(
            {
                "code": b.code,
                "name": b.name,
                "location": b.location,
                "image_url": f"{request.scheme}://{request.get_host()}{settings.MEDIA_URL}branches/{b.code.lower()}.jpg",
            }
        )

    return JsonResponse({"branches": data})


# -----------------------
# Helper functions
# -----------------------


def save_branch_image(branch_code, uploaded_file):
    filename = f"{branch_code.lower()}.jpg"
    folder = os.path.join(settings.MEDIA_ROOT, "branches")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    try:
        image = Image.open(uploaded_file)
    except Exception:
        return  # invalid image file, silently ignore

    # Convert ANY format to RGB so JPEG save is safe
    if image.mode not in ("RGB",):
        image = image.convert("RGB")

    target_width = 600
    target_height = 400

    img_ratio = image.width / image.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        new_height = image.height
        new_width = int(new_height * target_ratio)
    else:
        new_width = image.width
        new_height = int(new_width / target_ratio)

    left = (image.width - new_width) // 2
    top = (image.height - new_height) // 2
    right = left + new_width
    bottom = top + new_height

    image = image.crop((left, top, right, bottom))
    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.LANCZOS # type: ignore[attr-defined]

    image = image.resize((target_width, target_height), resample)


    # ALWAYS saved as .jpg
    image.save(path, "JPEG", quality=85, optimize=True)


def delete_branch_image(branch_code):
    filename = f"{branch_code.lower()}.jpg"
    path = os.path.join(settings.MEDIA_ROOT, "branches", filename)

    if os.path.isfile(path):
        os.remove(path)
