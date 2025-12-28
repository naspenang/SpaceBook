from django import forms
from website.models import Library, Campus, Branch
from django.utils import timezone



LIBRARY_TYPE_CHOICES = [
    ("", "Select Library Type"),
    ("Main Library", "Main Library"),
    ("Satellite Library", "Satellite Library"),
    ("Faculty Library", "Faculty Library"),
    ("Special Collection", "Special Collection"),
    ("Resource Centre", "Resource Centre"),
]



class LibraryForm(forms.ModelForm):
    campus_code = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "campus-select",
            }
        ),

    )



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate campus dropdown
        campuses = Campus.objects.all().order_by("campus_name")
        self.fields["campus_code"].choices = [
            ("", "Select Campus")
        ] + [
            (c.campus_code, c.campus_name)
            for c in campuses
        ]

        # Show branch name only (hide branch code)
        self.fields["branch"].label_from_instance = lambda obj: obj.name

        # Today's date
        today = timezone.now().date()

        # Default "Last Verified" to today (only for new records)
        if not self.instance.pk:
            self.fields["last_verified"].initial = today

        # Restrict date picker to today only
        self.fields["last_verified"].widget.attrs["min"] = today
        self.fields["last_verified"].widget.attrs["max"] = today





    def clean_last_verified(self):
        date = self.cleaned_data.get("last_verified")
        today = timezone.now().date()

        if date != today:
            raise forms.ValidationError("Last verified date must be today.")
        return date
    
    def clean_library_code(self):
        code = self.cleaned_data.get("library_code")

        if not code:
            return code

        qs = Library.objects.filter(library_code=code)

        # If editing, exclude current record
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Library code already exists.")

        return code




    branch = forms.ModelChoiceField(
        queryset=Branch.objects.all().order_by("name"),
        required=False,
        empty_label="Select Branch",
        widget=forms.Select(attrs={
            "class": "form-control",
            "id": "branch-select",
        }),
    )





    library_type = forms.ChoiceField(
        choices=LIBRARY_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"}),
    )



    class Meta:
        model = Library
        fields = [
            "library_code",
            "branch",
            "campus_code",
            "library_name",
            "short_name",
            "address",
            "city",
            "state",
            "postcode",
            "phone",
            "email",
            "website_url",
            "opening_hours",
            "weekend_hours",
            "notes",
            "latitude",
            "longitude",
            "source_url",
            "last_verified",
        ]

        widgets = {
            "library_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. LIB-PP-01"
            }),

            "library_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Full library name"
            }),

            "short_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Short name (optional)"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Street address"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "State"
            }),

            "postcode": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Postcode"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 04-1234567"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "library@example.edu.my"
            }),

            "website_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://library.example.edu.my"
            }),

            "opening_hours": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Mon–Fri: 8.30am – 5.00pm"
            }),

            "weekend_hours": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "Sat–Sun: Closed"
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Additional notes (optional)"
            }),

            "latitude": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "any",
                "placeholder": "Latitude"
            }),

            "longitude": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "any",
                "placeholder": "Longitude"
            }),

            "source_url": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "Source reference URL"
            }),

            "last_verified": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),
        }

