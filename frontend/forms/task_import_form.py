from django import forms

from todolist.models import Task


class TaskImportForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['url']