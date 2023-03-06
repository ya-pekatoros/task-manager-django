from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    class Roles(models.TextChoices):
        DEVELOPER = "developer"
        MANAGER = "manager"
        ADMIN = "admin"

    def validate_role_choices(value):
        if value not in dict(User.Roles.choices):
            raise ValidationError(
                f"{value} is not a valid role, valid roles: {dict(User.Roles.choices)}"
            )

    name = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=254)
    role = models.CharField(
        max_length=255,
        default=Roles.DEVELOPER,
        choices=Roles.choices,
        validators=[validate_role_choices],
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.role == self.Roles.ADMIN:
            self.is_staff = True
        super().save(*args, **kwargs)
