from django import forms
from wagtail.contrib.forms.forms import FormBuilder


class NormalizedFormBuilder(FormBuilder):
    def create_multiline_field(self, field, options):
        attrs = {"rows": "4"}
        return forms.CharField(widget=forms.Textarea(attrs=attrs), **options)

    def create_datetime_field(self, field, options):
        attrs = {"type": "datetime-local"}
        return forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs=attrs), **options)
