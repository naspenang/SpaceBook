# website/forms.py
from django import forms
from .models import Branch
from django.core.validators import FileExtensionValidator

LOCATION_TO_CODE = {
    "Johor": "J",
    "Kedah": "K",
    "Kelantan": "D",
    "Melaka": "M",
    "Negeri Sembilan": "N",
    "Pahang": "C",
    "Perak": "A",
    "Perlis": "R",
    "Pulau Pinang": "P",
    "Sabah": "S",
    "Sarawak": "Q",
    "Selangor": "B",
    "Shah Alam": "BA",
    "Terengganu": "T",
}

LOCATION_CHOICES = [("", "Select a location")] + [
    ("Johor", "Johor"),
    ("Kedah", "Kedah"),
    ("Kelantan", "Kelantan"),
    ("Melaka", "Melaka"),
    ("Negeri Sembilan", "Negeri Sembilan"),
    ("Pahang", "Pahang"),
    ("Perak", "Perak"),
    ("Perlis", "Perlis"),
    ("Pulau Pinang", "Pulau Pinang"),
    ("Sabah", "Sabah"),
    ("Sarawak", "Sarawak"),
    ("Selangor", "Selangor"),
    ("Shah Alam", "Shah Alam"),
    ("Terengganu", "Terengganu"),
]


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

    location = forms.ChoiceField(
        choices=LOCATION_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
            model = Branch
            fields = ["name", "location"]  # code is hidden
            widgets = {
                "name": forms.TextInput(attrs={
                    "class": "form-control",
                    "placeholder": "Branch name (e.g. UiTM Pulau Pinang)",
                }),
            }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    def save(self, commit=True):
        instance = super().save(commit=False)

        # ONLY generate code when creating a new branch
        if not instance.pk:
            location_name = instance.location
            plate = LOCATION_TO_CODE.get(location_name)

            if not plate:
                raise forms.ValidationError("Invalid location selected.")
            existing = Branch.objects.filter(code__startswith=plate)

            if not existing.exists():
                instance.code = plate
            else:
                numbers = []
                for b in existing:
                    suffix = b.code[len(plate):]
                    if suffix.isdigit():
                        numbers.append(int(suffix))

                next_number = max(numbers, default=0) + 1
                instance.code = f"{plate}{next_number}"

        if commit:
            instance.save()

        return instance
