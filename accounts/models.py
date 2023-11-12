import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)

    CUSTOM_ROLES = (
        ("Super Admin", "Super Admin"),
        ("Admin", "Admin"),
        ("Team Leader", "Team Leader"),
        ("Employee", "Employee"),
    )

    role = models.CharField(
        max_length=20,
        choices=CUSTOM_ROLES,
        default="todo",
    )
    phone = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    team_leader = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL
    )


def get_all_users(user):
    return (
        CustomUser.objects.filter(
            is_staff=False, is_superuser=False, team_leader=user
        ).all()
        if user.role != "Super Admin"
        else CustomUser.objects.filter(is_staff=False, is_superuser=False).all()
    )


class Shift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Shift from {self.start_time} to {self.start_time}"
