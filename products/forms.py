# forms.py
from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Product
        fields = ["name", "description"]
