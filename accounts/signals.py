from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserRole

@receiver(post_save, sender=User)
def assign_role_from_email(sender, instance, created, **kwargs):
    if not created:
        return

    email = instance.email.lower()

    # DEFAULT VALUES
    instance.is_staff = False
    instance.is_superuser = False

    # STUDENT
    if email.endswith("@student.uitm.edu.my"):
        role = "STUDENT"

    # STAFF
    elif email.endswith("@uitm.edu.my"):
        role = "STAFF"
        instance.is_staff = True

    # FALLBACK (optional)
    else:
        role = "STUDENT"

    instance.save()

    UserRole.objects.create(
        user=instance,
        role=role
    )
