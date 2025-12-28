from django import forms
from website.models import Campus


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = [
            "campus_code",
            "branch",
            "campus_name",
            "city",
            "state",
            "role",
        ]
        widgets = {
            "campus_code": forms.TextInput(attrs={"class": "form-control"}),
            "branch": forms.Select(attrs={"class": "form-control"}),
            "campus_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }
