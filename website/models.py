# website/models.py
from django.db import models


class Branch(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Campus(models.Model):
    ROLE_CHOICES = [
        ("HQ", "HQ"),
        ("Main Campus", "Main Campus"),
        ("Satellite Campus", "Satellite Campus"),
    ]
    branch_name = models.CharField(
        max_length=100, help_text="Main UiTM branch, e.g. UiTM Cawangan Pulau Pinang"
    )
    campus_name = models.CharField(max_length=150, help_text="Official campus name")
    city = models.CharField(
        max_length=100, help_text="City or district where the campus is located"
    )
    state = models.CharField(max_length=100, help_text="State in Malaysia")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    class Meta:
        ordering = ["branch_name", "campus_name"]
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"

    def __str__(self):
        return f"{self.campus_name} ({self.branch_name})"
