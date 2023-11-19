import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser, PermissionsMixin):
    id = models.CharField(
        primary_key=True, max_length=36, default=uuid.uuid4, editable=False
    )
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

    def is_online(self):
        # Check if last login is within the last 9 hours
        if self.last_login:
            return timezone.now() - self.last_login <= timezone.timedelta(hours=9)
        return False


def get_all_users(user):
    user_team_leaders = CustomUser.objects.filter(
        is_staff=False, is_superuser=False, team_leader=user
    ).all()
    user_team_leaders_employees = CustomUser.objects.filter(
        is_staff=False, is_superuser=False, team_leader__in=user_team_leaders
    ).all()
    return (
        user_team_leaders | user_team_leaders_employees
        if user.role != "Super Admin"
        else CustomUser.objects.filter(is_staff=False, is_superuser=False).all()
    )


class Shift(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Shift from {self.start_time} to {self.end_time}"
