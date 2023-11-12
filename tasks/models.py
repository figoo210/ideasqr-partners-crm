from django.db import models

from crm_lead_core.custom_models import TimestampedModel

# Create your models here.


class Task(TimestampedModel):
    # Choices for task states
    TASK_STATE_CHOICES = (
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    )

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True, blank=True)
    due_date = models.DateField(auto_now=False, auto_now_add=False)
    state = models.CharField(
        max_length=20,
        choices=TASK_STATE_CHOICES,
        default="todo",
    )

    # Relations
    from_user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="from_user_tasks",
    )
    to_user = models.ForeignKey(
        "accounts.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="to_user_tasks",
    )
