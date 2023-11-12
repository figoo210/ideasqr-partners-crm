from django import forms
from .models import Queue


class QueueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QueueForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
        self.fields["name"].required = True

    class Meta:
        model = Queue
        fields = ["name", "description"]
