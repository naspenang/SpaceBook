from django.shortcuts import render, get_object_or_404, redirect
from website.models import Campus
from website.forms import CampusForm

def campus_list(request):
    campuses = Campus.objects.all()
    return render(request, "website/campus/campus_list.html", {
        "campuses": campuses
    })

def campus_create(request):
    form = CampusForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("campus_list")

    return render(request, "website/campus/campus_form.html", {
        "form": form,
        "title": "Add Campus"
    })



def campus_edit(request, pk):
    campus = get_object_or_404(Campus, pk=pk)
    form = CampusForm(request.POST or None, instance=campus)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("campus_list")

    return render(request, "website/campus/campus_form.html", {
        "form": form,
        "title": "Edit Campus"
    })



def campus_delete(request, pk):
    campus = get_object_or_404(Campus, pk=pk)

    if request.method == "POST":
        campus.delete()
        return redirect("campus_list")

    return render(request, "website/campus/campus_delete.html", {
        "campus": campus
    })

