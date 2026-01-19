from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from website.models import Library
from website.forms.forms_library import LibraryForm
from website.utils import save_library_image
from django.shortcuts import get_object_or_404
import os
from django.conf import settings
from website.models import Library, Campus, Branch





def library_list(request):
    filters_visible = request.GET.get("filters", "1") != "0"
    embed = request.GET.get("embed") == "1"
    base_template = "website/embed_base.html" if embed else "website/base.html"


    branch_code = request.GET.get("branch")
    campus_code = request.GET.get("campus")

    # If branch is not selected, ignore campus
    if not branch_code:
        campus_code = None

    libraries = Library.objects.all()

    # Branch filter (via Campus)
    if branch_code:
        campus_codes = (
            Campus.objects
            .filter(branch__code=branch_code)
            .values_list("campus_code", flat=True)
        )
        libraries = libraries.filter(campus_code__in=campus_codes)

    # Campus filter (more specific)
    if campus_code:
        libraries = libraries.filter(campus_code=campus_code)

    # Branch dropdown (first)
    branches = Branch.objects.all().order_by("name")

    # Campus dropdown depends on branch
    if branch_code:
        campuses = (
            Campus.objects
            .filter(branch__code=branch_code)
            .order_by("campus_name")
        )
    else:
        campuses = Campus.objects.none()


    # Build embed querystring cleanly
    embed_params = request.GET.copy()
    embed_params["filters"] = "0"
    embed_params["embed"] = "1"

    embed_querystring = embed_params.urlencode()


    return render(
        request,
        "website/library/library_list.html",
        {
            "libraries": libraries,
            "branches": branches,
            "campuses": campuses,
            "selected_branch": branch_code,
            "selected_campus": campus_code,
            "filters_visible": filters_visible,
            "base_template": base_template,
            "embed_querystring": embed_querystring,
        }
    )







def library_detail(request, library_code):
    library = get_object_or_404(Library, library_code=library_code)

    return render(
        request,
        "website/library/library_detail.html",
        {
            "library": library
        }
    )


@login_required
def library_edit(request, library_code):
    library = get_object_or_404(Library, library_code=library_code)
    form = LibraryForm(request.POST or None, request.FILES or None, instance=library)

    if request.method == "POST" and form.is_valid():
        library = form.save()

        image = request.FILES.get("image")
        if image:
            save_library_image(library.library_code, image)

        return redirect("library_detail", library_code=library.library_code)

    return render(
        request,
        "website/library/library_form.html",
        {
            "form": form,
            "title": "Edit Library",
        }
    )



@login_required
def library_create(request):
    form = LibraryForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        library = form.save()

        image = request.FILES.get("image")
        if image:
            save_library_image(library.library_code, image)

        return redirect("library_list")

    return render(
        request,
        "website/library/library_form.html",
        {
            "form": form,
            "title": "Add Library",
        }
    )


@login_required
@login_required
def library_delete(request, library_code):
    library = get_object_or_404(Library, library_code=library_code)

    if request.method == "POST":
        # Delete image file if it exists
        image_path = os.path.join(
            settings.MEDIA_ROOT,
            "libraries",
            f"{library.library_code}.jpg"
        )

        if os.path.exists(image_path):
            os.remove(image_path)

        library.delete()
        return redirect("library_list")

    return render(
        request,
        "website/library/library_delete.html",
        {
            "library": library
        }
    )

