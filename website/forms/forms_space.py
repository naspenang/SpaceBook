from django import forms
from django.core.validators import FileExtensionValidator
from website.validators import validate_image_size
from website.models import LibrarySpace


class LibrarySpaceForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
        ],
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control"}
        ),
    )

    class Meta:
        model = LibrarySpace
        fields = [
            "library",
            "space_name",
            "image",
            "description",
            "room_number",
            "floor",
            "capacity",
            "space_type",
            "noise_level",
            "has_projector",
            "has_whiteboard",
            "has_wifi",
            "has_power_plug",
            "has_network_node",
            "wheelchair_accessible",
            "has_climate_control",
            "is_active",
            "available_from",
            "available_to",
            "buffer_minutes",
            "advance_notice",
            "requires_approval",
            "requires_payment",
            "fee_amount",
            "access_policy",
            "booking_notes",
        ]

        widgets = {
            # ---- BASIC ----
            "library": forms.Select(attrs={
                "class": "form-control",
            }),

            "space_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Design Discussion Room",
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Brief description of the space",
            }),

            # ---- LOCATION ----
            "room_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. DES-01",
            }),

            "floor": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Level 2",
            }),

            "capacity": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "placeholder": "e.g. 12",
            }),

            # ---- CLASSIFICATION ----
            "space_type": forms.Select(attrs={
                "class": "form-control",
            }),

            "noise_level": forms.Select(attrs={
                "class": "form-control",
            }),

            # ---- TIME / RULES ----
            "available_from": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time",
            }),

            "available_to": forms.TimeInput(attrs={
                "class": "form-control",
                "type": "time",
            }),

            "buffer_minutes": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "placeholder": "e.g. 15",
            }),

            "advance_notice": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 0,
                "placeholder": "Hours in advance",
            }),

            "fee_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "placeholder": "RM",
            }),

            "access_policy": forms.Select(attrs={
                "class": "form-control",
            }),

            "booking_notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Additional booking notes (optional)",
            }),
        }
