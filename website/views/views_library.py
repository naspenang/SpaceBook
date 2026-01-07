from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from website.models import Library
from website.forms.forms_library import LibraryForm
from django.shortcuts import get_object_or_404



def library_list(request):
    libraries = Library.objects.all().order_by("library_name")

    return render(
        request,
        "website/library/library_list.html",
        {
            "libraries": libraries
        }
    )



@login_required
def library_create(request):
    form = LibraryForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
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
def library_delete(request, library_code):
    library = get_object_or_404(Library, library_code=library_code)

    if request.method == "POST":
        library.delete()
        return redirect("library_list")

    return render(request, "website/library/library_delete.html", {
        "library": library
    })
