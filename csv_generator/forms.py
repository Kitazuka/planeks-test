from crispy_forms.helper import FormHelper
from django import forms

from .models import Schema, Columns


class SchemaCreateForm(forms.ModelForm):
    class Meta:
        model = Schema
        fields = ["name", "separator", "string_character"]


class ColumnsForm(forms.ModelForm):
    class Meta:
        model = Columns
        fields = ("column_name", "type", "order")


class RowsForm(forms.Form):
    rows = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_show_labels = False
