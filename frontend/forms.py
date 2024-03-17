from django import forms

from todolist.models import TodoList, Task


class TodolistForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['name', 'description', 'tasks']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'deadline', 'importance', 'file', 'image', "done"]


class TaskImportForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['url']
