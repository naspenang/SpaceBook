# website/models.py
from django.db import models

# ------------------------------
# Branch Model
# ------------------------------
class Branch(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


# ------------------------------
# Campus Model
# ------------------------------
class Campus(models.Model):
    ROLE_CHOICES = [
        ("HQ", "HQ"),
        ("Main Campus", "Main Campus"),
        ("Satellite Campus", "Satellite Campus"),
    ]

    campus_code = models.CharField(
        max_length=20, primary_key=True, help_text="Unique campus identifier"
    )

    branch = models.ForeignKey(
        Branch,
        to_field="code",
        db_column="branch_code",
        on_delete=models.PROTECT,
        related_name="campuses",
    )

    campus_name = models.CharField(max_length=150, help_text="Official campus name")

    city = models.CharField(max_length=100, blank=True)

    state = models.CharField(max_length=100, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        db_table = "website_campus"
        ordering = ["campus_name"]
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"

    def __str__(self):
        return f"{self.campus_name} ({self.campus_code})"


# ------------------------------
# Library Model
# ------------------------------
class Library(models.Model):
    # PRIMARY KEY
    library_code = models.CharField(max_length=50, primary_key=True)

    # Optional relationship-ish field (kept as plain text to match your schema)
    campus_code = models.CharField(max_length=150, blank=True, null=True)

    library_name = models.TextField()
    short_name = models.TextField(blank=True, null=True)
    library_type = models.TextField(blank=True, null=True)

    address = models.TextField(blank=True, null=True)
    city = models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    postcode = models.TextField(blank=True, null=True)

    phone = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    opening_hours = models.TextField(blank=True, null=True)
    weekend_hours = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    source_url = models.URLField(blank=True, null=True)
    last_verified = models.DateField(blank=True, null=True)

    class Meta:
        db_table = "website_library"
        ordering = ["library_name"]
        verbose_name = "Library"
        verbose_name_plural = "Libraries"

    def __str__(self):
        return f"{self.library_name} ({self.library_code})"



# ------------------------------
# Library Space Model
# ------------------------------
class LibrarySpace(models.Model):

    # --- Choice definitions ---
    SPACE_TYPES = [
        ("study", "Study Area"),
        ("discussion", "Discussion Room"),
        ("media", "Media / Lab"),
        ("reading", "Reading Area"),
        ("other", "Other"),
    ]

    NOISE_LEVELS = [
        ("quiet", "Quiet"),
        ("moderate", "Moderate"),
        ("loud", "Loud"),
    ]

    ACCESS_POLICIES = [
        ("public", "Public"),
        ("students", "Students Only"),
        ("staff", "Staff Only"),
        ("restricted", "Restricted"),
    ]

    # --- Identity ---
    space_id = models.AutoField(primary_key=True)

    library = models.ForeignKey(
        Library,
        to_field="library_code",
        db_column="library_code",
        on_delete=models.CASCADE,
        related_name="spaces"
    )


    space_name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    floor = models.CharField(max_length=50, blank=True)
    space_type = models.CharField(
        max_length=20,
        choices=SPACE_TYPES,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    # --- Physical attributes ---
    capacity = models.PositiveIntegerField()
    has_projector = models.BooleanField(default=False)
    has_whiteboard = models.BooleanField(default=False)
    wheelchair_accessible = models.BooleanField(default=False)
    has_climate_control = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_power_plug = models.BooleanField(default=False)
    has_network_node = models.BooleanField(default=False)


    noise_level = models.CharField(
        max_length=20,
        choices=NOISE_LEVELS,
        blank=True
    )

    # --- Operational rules ---
    available_from = models.TimeField()
    available_to = models.TimeField()

    buffer_minutes = models.PositiveIntegerField(default=0)
    advance_notice = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Hours before booking"
    )

    requires_payment = models.BooleanField(default=False)
    fee_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    # --- Policy ---
    requires_approval = models.BooleanField(default=False)

    access_policy = models.CharField(
        max_length=20,
        choices=ACCESS_POLICIES,
        default="public"
    )

    booking_notes = models.TextField(blank=True)

    # --- Metadata ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_use = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "website_space"
        ordering = ["space_name"]

    def __str__(self):
        return f"{self.space_name} ({self.library.library_code})"
