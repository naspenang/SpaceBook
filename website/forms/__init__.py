from django import forms
from website.models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = [
            "booking_date",
            "start_time",
            "end_time",
        ]

        widgets = {
            "booking_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "start_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),
            "end_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),
        }

        labels = {
            "booking_date": "Date",
            "start_time": "Start time",
            "end_time": "End time",
        }
