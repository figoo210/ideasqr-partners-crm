# forms.py
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["to_user"].required = True
        self.fields["to_user"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"

        self.fields["due_date"].widget = forms.SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
        )

        self.fields["from_user"].required = False

    class Meta:
        model = Task
        fields = ["name", "description", "due_date", "from_user", "to_user"]
