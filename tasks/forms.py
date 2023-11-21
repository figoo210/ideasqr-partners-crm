# forms.py
from django import forms

from accounts.models import CustomUser
from .models import Task


class TaskForm(forms.ModelForm):
    username = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["to_user"].required = False
        self.fields["to_user"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"

        self.fields["due_date"].widget = forms.SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
        )

        self.fields["from_user"].required = False

    def save(self, commit=True):
        # Get the instance of CustomUser but don't save it yet
        task = super(TaskForm, self).save(commit=False)
        task.to_user = CustomUser.objects.filter(
            username=self.cleaned_data["username"]
        ).first()
        if commit:
            task.save()
        return task

    class Meta:
        model = Task
        fields = ["name", "description", "due_date", "from_user", "to_user"]
