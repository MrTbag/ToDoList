from django import forms
from .models import List, Task


class ListForm(forms.Form):
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=50)
    tasks = forms.ModelMultipleChoiceField(queryset=Task.objects)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'importance', 'deadline']
