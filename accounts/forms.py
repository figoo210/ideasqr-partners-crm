from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.forms.widgets import SelectDateWidget

from .models import CustomUser, Shift


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if field_name in [
                "first_name",
                "last_name",
                "username",
                "email",
                "phone",
                "birth_date",
                "password1",
                "password2",
            ]:
                field.required = True
        self.fields["password"].required = False
        self.fields["date_joined"].required = False
        self.fields["birth_date"].widget = SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
            years=[str(year) for year in range(1950, 2021)],
        )

    class Meta:
        model = CustomUser
        fields = "__all__"


update_fields = [
    "first_name",
    "last_name",
    "username",
    "email",
    "phone",
    "birth_date",
    "role",
    "image",
    "team_leader",
]


class UpdateUserForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if field_name in update_fields and field_name != "image":
                field.required = True
        self.fields["birth_date"].widget = SelectDateWidget(
            empty_label=("Year", "Month", "Day"),
            years=[str(year) for year in range(1950, 2021)],
        )
        self.fields["role"].required = False
        self.fields["team_leader"].required = False
        # self.new_password.is_required = False

    class Meta:
        model = CustomUser
        fields = update_fields


class ShiftForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(ShiftForm, self).__init__(*args, **kwargs)

        self.fields["start_time"].required = True
        self.fields["start_time"].widget.attrs["class"] = "form-control"

        self.fields["end_time"].required = True
        self.fields["end_time"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Shift
        fields = ["start_time", "end_time"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }
