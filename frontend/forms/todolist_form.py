from django import forms

from todolist.models import TodoList


class TodolistForm(forms.ModelForm):
    class Meta:
        model = TodoList
        fields = ['name', 'description', 'tasks']
