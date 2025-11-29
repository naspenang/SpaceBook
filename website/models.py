from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=100, blank=True)
    code = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
