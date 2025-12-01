from django.db import models


from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True, null=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(
        upload_to="branches/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
