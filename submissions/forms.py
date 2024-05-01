from django import forms

from products.models import Product, SubmissionProducts

from .models import Closers, LeaderStatus, Submission, Status

from datetime import datetime
import pytz


class ProductCountForm(forms.ModelForm):
    class Meta:
        model = SubmissionProducts
        fields = ["product", "count"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class AddSubmissionForm(forms.ModelForm):
    POS_TYPE_CHOICES = [
        ("POS2", "POS2"),
        ("POS4", "POS4"),
    ]
    pos_type = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=POS_TYPE_CHOICES,
    )

    class Meta:
        model = Submission
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

        self.fields["birth_date"].widget = forms.SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
            years=[str(year) for year in range(1950, 2021)],
        )
        self.fields["address"].widget.attrs["rows"] = 5
        self.fields["products"].widget.attrs["class"] = "form-control-custom"


class StatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StatusForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["name"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Status
        fields = ["name"]


class LeaderStatusForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LeaderStatusForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["name"].widget.attrs["class"] = "form-control"

    class Meta:
        model = LeaderStatus
        fields = ["name"]


class CloserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CloserForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["name"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Closers
        fields = ["name"]
