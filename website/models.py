from django.db import models


class Branch(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
