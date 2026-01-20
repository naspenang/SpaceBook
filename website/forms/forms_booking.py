from django import forms
from django.db.models import Q
from website.models import Booking


class BookingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # we will pass space from the view
        self.space = kwargs.pop("space", None)
        super().__init__(*args, **kwargs)

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

    def clean(self):
        cleaned_data = super().clean()

        booking_date = cleaned_data.get("booking_date")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # basic time validation (already added, but keep it here)
        if start_time and end_time and end_time <= start_time:
            self.add_error(
                "end_time",
                "End time must be later than start time."
            )
            return cleaned_data

        # conflict detection
        if self.space and booking_date and start_time and end_time:
            conflicts = Booking.objects.filter(
                space=self.space,
                booking_date=booking_date,
            ).exclude(
                status__in=["CANCELLED", "REJECTED"]
            ).filter(
                Q(start_time__lt=end_time) &
                Q(end_time__gt=start_time)
            )

            if conflicts.exists():
                raise forms.ValidationError(
                    "This time slot is already booked. Please choose another time."
                )

        return cleaned_data
