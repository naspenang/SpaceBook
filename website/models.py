# website/models.py
from django.db import models

#------------------------------
# Branch Model
#------------------------------
class Branch(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


#------------------------------
# Campus Model
#------------------------------
class Campus(models.Model):
    ROLE_CHOICES = [
        ("HQ", "HQ"),
        ("Main Campus", "Main Campus"),
        ("Satellite Campus", "Satellite Campus"),
    ]

    campus_code = models.CharField(
        max_length=20,
        primary_key=True,
        help_text="Unique campus identifier"
    )

    branch = models.ForeignKey(
        Branch,
        to_field="code",
        db_column="branch_code",
        on_delete=models.PROTECT,
        related_name="campuses",
    )


    campus_name = models.CharField(
        max_length=150,
        help_text="Official campus name"
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    class Meta:
        db_table = "website_campus"
        ordering = ["campus_name"]
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"

    def __str__(self):
        return f"{self.campus_name} ({self.campus_code})"
