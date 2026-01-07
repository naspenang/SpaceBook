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
        "campus_code": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Campus Code"
        }),
        "campus_name": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Campus Name"
        }),
        "city": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "City"
        }),
        "state": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "State"
        }),
    }

