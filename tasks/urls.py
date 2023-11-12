# urls.py
from django.urls import path
from .views import (
    TaskListView,
    TaskCreateView,
    TaskUpdateView,
    delete_task,
    update_task_state,
)

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("add-task", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:id>/delete/", delete_task, name="task-update"),
    path(
        "task/state/<int:id>/<str:state>", update_task_state, name="task-state-update"
    ),
]
