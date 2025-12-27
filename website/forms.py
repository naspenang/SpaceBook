# website/forms.py
from django import forms
from .models import Branch
from .models import Campus
from django.core.validators import FileExtensionValidator


LOCATION_TO_CODE = {}


def load_location_codes():
    LOCATION_TO_CODE.clear()
    for b in Branch.objects.all():
        if b.location and b.code:
            LOCATION_TO_CODE[b.location] = b.code


def get_location_choices():
    locations = (
        Branch.objects.exclude(location__isnull=True)
        .exclude(location__exact="")
        .values_list("location", flat=True)
        .distinct()
    )

    return [("", "Select a location")] + [(loc, loc) for loc in locations]


def validate_image_size(image):
    max_size = 10
    mb_converted = max_size * 1024 * 1024
    if image.size > mb_converted:
        raise forms.ValidationError(f"Image file too large (maximum {max_size}MB).")


class BranchForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
        ],
        widget=forms.ClearableFileInput(attrs={"class": "form-control"}),
        label="Branch Image (optional)",
    )

    location = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Branch
        fields = ["name", "location"]  # code is hidden
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Branch name (e.g. UiTM Pulau Pinang)",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        load_location_codes()
        self.fields["location"].choices = get_location_choices()

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
                    suffix = b.code[len(plate) :]
                    if suffix.isdigit():
                        numbers.append(int(suffix))

                next_number = max(numbers, default=0) + 1
                instance.code = f"{plate}{next_number}"

        if commit:
            instance.save()

        return instance


from .models import Campus, Branch


class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ["campus_code", "branch", "campus_name", "city", "state", "role"]
        widgets = {
            "campus_code": forms.TextInput(attrs={"class": "form-control"}),
            "branch": forms.Select(attrs={"class": "form-control"}),
            "campus_name": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "state": forms.TextInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
        }
