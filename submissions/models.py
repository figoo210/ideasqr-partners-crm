from django.db import models
from django.db.models import Q
from crm_lead_core.custom_models import TimestampedModel, CreatedByMixin


class Status(TimestampedModel):
    name = models.CharField(primary_key=True, max_length=100)


class Submission(TimestampedModel, CreatedByMixin):
    medical_id = models.CharField(max_length=11)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_initial = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=10)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    comment = models.TextField(null=True, blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    user_queue = models.ForeignKey(
        "queues.UserQueue",
        on_delete=models.SET_NULL,
        null=True,
    )
    products = models.ManyToManyField(
        "products.Product", blank=True, through="products.SubmissionProducts"
    )


def get_submissions_based_on_role(user, user_team_leaders, user_team_leaders_employees):
    """
    Get submissions based on the role of the logged in user
    :param user: The current logged-in user
    :return: A QuerySet containing all submissions for that particular role
    """
    if user.role == "Super Admin":
        return Submission.objects.all().order_by("-created_at")
    elif user.role == "Admin":
        # Fetch submissions for the Admin, their Team Leaders, and Team Leader's Employees
        admin_submissions = Submission.objects.filter(
            Q(user_queue__user=user)
        ).order_by("-created_at")
        team_leader_submissions = Submission.objects.filter(
            Q(user_queue__user__in=user_team_leaders)
        ).order_by("-created_at")
        team_leader_employees_submissions = Submission.objects.filter(
            Q(user_queue__user__in=user_team_leaders_employees)
        ).order_by("-created_at")

        # Combine all QuerySets
        all_submissions = (
            admin_submissions
            | team_leader_submissions
            | team_leader_employees_submissions
        )

        return all_submissions
    elif user.role == "Team Leader":
        # Fetch submissions for the Team Leader and their Employees
        team_leader_submissions = Submission.objects.filter(
            Q(user_queue__user=user)
        ).order_by("-created_at")
        team_leader_employees_submissions = Submission.objects.filter(
            Q(user_queue__user__in=user_team_leaders)
        ).order_by("-created_at")

        # Combine both QuerySets
        all_submissions = team_leader_submissions | team_leader_employees_submissions

        return all_submissions
    elif user.role == "Employee":
        # Fetch submissions for the Employee
        employee_submissions = Submission.objects.filter(
            Q(user_queue__user=user)
        ).order_by("-created_at")

        return employee_submissions
    else:
        raise ValueError("Invalid Role!")
