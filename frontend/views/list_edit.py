from django.shortcuts import render, get_object_or_404

from todolist.models import TodoList
from frontend.forms import TodolistForm


def list_edit(request, list_id):
    if request.method == 'GET':
        prev_list = get_object_or_404(TodoList, id=list_id)
        form = TodolistForm(
            {'name': prev_list.name, 'description': prev_list.description, 'tasks': prev_list.tasks.all()})
        return render(request, 'frontend/list_form_edit.html', {"form": form, "list_id": list_id})

    return render(request, 'frontend/wrong_method.html')
