from django.urls import path
from .views import (
    StatusCreateView,
    StatusListView,
    StatusUpdateView,
    SubmissionsView,
    AddSubmissionView,
    UpdateSubmissionView,
    update_submission_status,
    update_submission_comment,
    add_submission_feedback,
    delete_status,
)

urlpatterns = [
    path("submissions", SubmissionsView.as_view(), name="Submissions"),
    path(
        "supmissions/status/<int:id>/<str:status>",
        update_submission_status,
        name="submissions_status_update",
    ),
    path(
        "supmissions/comment/update",
        update_submission_comment,
        name="submissions_comment_update",
    ),
    path(
        "supmissions/feedback/add",
        add_submission_feedback,
        name="submissions_feedbacking",
    ),
    path("add-submission", AddSubmissionView.as_view(), name="add_submission"),
    path(
        "submissions/<int:pk>/update",
        UpdateSubmissionView.as_view(),
        name="update_submission",
    ),
    path("status/", StatusListView.as_view(), name="status_list"),
    path("status/create", StatusCreateView.as_view(), name="status_create"),
    path("status/<str:pk>/update", StatusUpdateView.as_view(), name="status_update"),
    path("status/<str:status_name>/delete", delete_status, name="status_delete"),
]
