from django.db import models

from crm_lead_core.custom_models import CreatedByMixin, TimestampedModel


class Queue(TimestampedModel, CreatedByMixin):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    user = models.ManyToManyField("accounts.CustomUser", through="UserQueue")


class UserQueue(TimestampedModel):
    user = models.ForeignKey(
        "accounts.CustomUser", on_delete=models.SET_NULL, null=True
    )
    queue = models.ForeignKey(Queue, on_delete=models.SET_NULL, null=True)
    website = models.CharField(max_length=255, null=True, blank=True)

    # shift_start = models.TimeField(
    #     auto_now=False,
    #     auto_now_add=False,
    #     null=True,
    #     blank=True,
    # )
    # shift_end = models.TimeField(
    #     auto_now=False,
    #     auto_now_add=False,
    #     null=True,
    #     blank=True,
    # )
