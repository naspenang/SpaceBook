from django.shortcuts import render, get_object_or_404, redirect
from website.models import Campus
from website.forms.forms_campus import CampusForm
from django.http import JsonResponse


def campus_list(request):
    campuses = Campus.objects.all()
    return render(request, "website/campus/campus_list.html", {"campuses": campuses})


def campus_create(request):
    form = CampusForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("campus_list")

    return render(
        request,
        "website/campus/campus_form.html",
        {"form": form, "title": "Add Campus"},
    )


def campus_edit(request, campus_code):
    campus = get_object_or_404(Campus, campus_code=campus_code)
    form = CampusForm(request.POST or None, instance=campus)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("campus_list")

    return render(
        request,
        "website/campus/campus_form.html",
        {"form": form, "title": "Edit Campus"},
    )


def campus_delete(request, campus_code):
    campus = get_object_or_404(Campus, campus_code=campus_code)

    if request.method == "POST":
        branch_code = campus.branch.code
        campus.delete()
        return redirect("branch_detail", code=branch_code)

    return render(request, "website/campus/campus_delete.html", {"campus": campus})


# -----------------------
#  API
# -----------------------


def campus_by_branch_api(request):
    branch_code = request.GET.get("branch")

    data = []

    if branch_code:
        campuses = Campus.objects.filter(branch__code=branch_code).order_by(
            "campus_name"
        )

        for c in campuses:
            data.append(
                {
                    "campus_code": c.campus_code,
                    "campus_name": c.campus_name,
                }
            )

    return JsonResponse({"campuses": data})
