from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from website.models import Library
from website.forms.forms_library import LibraryForm
from website.utils import save_library_image
from django.shortcuts import get_object_or_404
import os
from django.conf import settings




def library_list(request):
    libraries = Library.objects.all().order_by("library_name")

    return render(
        request,
        "website/library/library_list.html",
        {
            "libraries": libraries
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

