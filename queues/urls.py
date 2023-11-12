from django.urls import path
from .views import (
    QueueCreateView,
    QueueUpdateView,
    QueueListView,
    delete_queue,
    update_queue_user,
    update_queue_website,
)

urlpatterns = [
    path("queues/create", QueueCreateView.as_view(), name="queue-create"),
    path("queues/<int:pk>/update", QueueUpdateView.as_view(), name="queue-update"),
    path("queues/<int:queue_id>/delete", delete_queue, name="queue-delete"),
    path("update-queue-website", update_queue_website, name="update-queue-website"),
    path(
        "queues/assign/<int:queue_id>/<str:user_id>",
        update_queue_user,
        name="queue-user-assign",
    ),
    path("queues", QueueListView.as_view(), name="queues-list"),
]
