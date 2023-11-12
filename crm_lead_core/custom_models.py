from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class CreatedByMixin(models.Model):
    created_by = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="%(app_label)s_%(class)s_created_by_related",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:  # Only set the user on creation
            self.created_by = get_current_user()
        super().save(*args, **kwargs)


def get_current_user():
    from django.contrib.auth import get_user

    user = get_user()
    return user if user and user.is_authenticated else None
