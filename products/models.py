from django.db import models

from crm_lead_core.custom_models import TimestampedModel

# Create your models here.


class Product(TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, blank=True)
    submissions = models.ManyToManyField(
        "submissions.Submission", through="products.SubmissionProducts"
    )

    def __str__(self):
        """
        String representation
        """
        return f"{self.name}"


class SubmissionProducts(TimestampedModel):
    count = models.SmallIntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    submission = models.ForeignKey(
        "submissions.Submission",
        related_name="submission_products",
        on_delete=models.SET_NULL,
        null=True,
    )
