# website/forms/forms_space.py
from django import forms
from website.models import LibrarySpace

class LibrarySpaceForm(forms.ModelForm):
    class Meta:
        model = LibrarySpace
        fields = [
            "library",
            "space_name",
            "description",
            "room_number",
            "floor",
            "space_type",
            "is_active",
            "capacity",
            "has_projector",
            "has_whiteboard",
            "has_wifi",
            "has_power_plug",
            "has_network_node",
            "wheelchair_accessible",
            "has_climate_control",
            "noise_level",
            "available_from",
            "available_to",
            "buffer_minutes",
            "advance_notice",
            "requires_payment",
            "fee_amount",
            "requires_approval",
            "access_policy",
            "booking_notes",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "booking_notes": forms.Textarea(attrs={"rows": 3}),
            "available_from": forms.TimeInput(attrs={"type": "time"}),
            "available_to": forms.TimeInput(attrs={"type": "time"}),
        }
