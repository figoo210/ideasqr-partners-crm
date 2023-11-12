from django.db import models

from crm_lead_core.custom_models import TimestampedModel

# Create your models here.


class Feedback(TimestampedModel):
    content = models.CharField(max_length=255)

    # Relations
    user = models.ForeignKey(
        "accounts.CustomUser",
        related_name="user_feedbacks",  # Add related_name for clarity
        on_delete=models.SET_NULL,
        null=True,
    )
    submission = models.ForeignKey(
        "submissions.Submission",
        related_name="submission_feedbacks",  # Add related_name for clarity
        on_delete=models.SET_NULL,
        null=True,
    )
