from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
import uuid


class NonDeletedManager(models.Manager):
    """
    Custom manager to retrieve non-deleted records by default.
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    date = models.DateField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        """
        Override the delete method to perform soft delete.
        """
        self.is_deleted = True
        self.save()

    def undelete(self, *args, **kwargs):
        """
        Method to undo soft delete and restore the object.
        """
        self.is_deleted = False
        self.save()

    objects = NonDeletedManager()


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
        if not self.id and "request" in kwargs:  # Only set the user on creation
            request = kwargs.pop("request")
            self.created_by = get_current_user(request)
        super().save(*args, **kwargs)


def get_current_user(request):
    user = request.user if request.user.is_authenticated else None
    return user
