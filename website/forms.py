# website/forms.py
from django import forms
from .models import Branch


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ["name", "state", "code", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. UiTM Cawangan Pulau Pinang",
                }
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Pulau Pinang",
                }
            ),
            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. PPN",
                }
            ),
        }
        labels = {
            "name": "Branch Name",
            "state": "State",
            "code": "Branch Code",
            "image": "Branch Image",
        }
