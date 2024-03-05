from django import forms
from .models import UrlDict


class UrlForm(forms.ModelForm):
    class Meta:
        model = UrlDict
        fields = ['original_url', ]
