from django import forms

from todolist.models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'deadline', 'importance', 'file', 'image', "done"]
