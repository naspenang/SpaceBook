# website/forms.py
from django import forms
from .models import Branch
from django.core.validators import FileExtensionValidator


def validate_image_size(image):
    max_size = 2
    mb_converted = max_size * 1024 * 1024
    if image.size > mb_converted:
        raise forms.ValidationError(f"Image file too large (maximum {max_size}MB).")


class BranchForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(["jpg"]),
            validate_image_size,
        ],
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Branch Image (optional)",
    )

    class Meta:
        model = Branch
        fields = ["name", "state", "code"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["code"].disabled = True
