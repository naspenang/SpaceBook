# website/views/views_space.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from website.models import LibrarySpace, Library, Campus
from website.forms.forms_space import LibrarySpaceForm
from django.conf import settings


def space_list(request):
    library_code = request.GET.get("library")
    campus_code = request.GET.get("campus")
    embed = request.GET.get("embed")
    is_embed = bool(embed)

    has_projector = request.GET.get("projector")
    accessible = request.GET.get("accessible")
    has_wifi = request.GET.get("wifi")
    has_power = request.GET.get("power")
    has_network = request.GET.get("network")
    has_whiteboard = request.GET.get("whiteboard")
    

    spaces = LibrarySpace.objects.select_related("library").order_by("space_name")

    selected_library = None
    selected_campus = None

    if has_projector:
        spaces = spaces.filter(has_projector=True)

    if accessible:
        spaces = spaces.filter(wheelchair_accessible=True)

    if has_wifi:
        spaces = spaces.filter(has_wifi=True)

    if has_power:
        spaces = spaces.filter(has_power_plug=True)

    if has_network:
        spaces = spaces.filter(has_network_node=True)

    if has_whiteboard:
        spaces = spaces.filter(has_whiteboard=True)

    if campus_code:
        selected_campus = campus_code
        spaces = spaces.filter(library__campus_code=campus_code)

    if library_code:
        selected_library = get_object_or_404(Library, library_code=library_code)
        spaces = spaces.filter(library=selected_library)

    campuses = Campus.objects.order_by("campus_name")
    libraries = Library.objects.all().order_by("library_name")

    if campus_code:
        libraries = libraries.filter(campus_code=campus_code)

    base_template = "website/embed_base.html" if embed else "website/base.html"

    # Build embed querystring while preserving filters
    querydict = request.GET.copy()
    querydict["embed"] = "1"
    embed_querystring = querydict.urlencode()

    return render(request, "website/space/space_list.html", {
        "spaces": spaces,
        "campuses": campuses,
        "libraries": libraries,
        "selected_campus": selected_campus,
        "selected_library": selected_library,
        "base_template": base_template,
        "filters_visible": True,
        "embed_querystring": embed_querystring,
        "has_projector": has_projector,
        "accessible": accessible,
        "has_wifi": has_wifi,
        "has_power": has_power,
        "has_network": has_network,
        "has_whiteboard": has_whiteboard,
        "is_embed": is_embed,
    })



def space_detail(request, space_id):
    space = get_object_or_404(LibrarySpace, space_id=space_id)
    return render(request, "website/space/space_detail.html", {"space": space})


@login_required
def space_create(request):
    preset_library_code = request.GET.get("library")
    initial = {}

    if preset_library_code:
        initial["library"] = get_object_or_404(Library, library_code=preset_library_code)

    if request.method == "POST":
        form = LibrarySpaceForm(request.POST, request.FILES, initial=initial)
        if form.is_valid():
            space = form.save()

            image = form.cleaned_data.get("image")
            if image:
                space_dir = os.path.join(settings.MEDIA_ROOT, "spaces")
                os.makedirs(space_dir, exist_ok=True)

                image_path = os.path.join(space_dir, f"{space.space_id}.jpg")
                with open(image_path, "wb+") as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

            return redirect("space_detail", space_id=space.space_id)
    else:
        form = LibrarySpaceForm(initial=initial)

    return render(request, "website/space/space_form.html", {
        "form": form,
        "title": "Add Space",
    })


@login_required
def space_edit(request, space_id):
    space = get_object_or_404(LibrarySpace, space_id=space_id)

    if request.method == "POST":
        form = LibrarySpaceForm(request.POST, request.FILES, instance=space)
        if form.is_valid():
            space = form.save()

            image = form.cleaned_data.get("image")
            if image:
                space_dir = os.path.join(settings.MEDIA_ROOT, "spaces")
                os.makedirs(space_dir, exist_ok=True)

                image_path = os.path.join(space_dir, f"{space.space_id}.jpg")
                with open(image_path, "wb+") as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)

            return redirect("space_detail", space_id=space.space_id)
    else:
        form = LibrarySpaceForm(instance=space)

    return render(request, "website/space/space_form.html", {
        "form": form,
        "title": "Edit Space",
    })



@login_required
def space_delete(request, space_id):
    space = get_object_or_404(LibrarySpace, space_id=space_id)

    if request.method == "POST":
        image_path = os.path.join(settings.MEDIA_ROOT, "spaces", f"{space.space_id}.jpg")
        if os.path.exists(image_path):
            os.remove(image_path)

        space.delete()
        return redirect("space_list")

    return render(request, "website/space/space_delete.html", {"space": space})
