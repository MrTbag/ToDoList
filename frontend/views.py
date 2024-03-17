import json
import re

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View

from url_shortener.models import UrlDict

from todolist.models import CustomUser, TodoList, Task
from frontend.forms import TodolistForm, TaskForm


class IndexView(View):
    def get(self, request):
        user: CustomUser = request.user
        lists = user.todolist_set.all()
        context = {
            'lists': lists,
            'user': request.user.username
        }
        return render(request, 'frontend/todolist_list.html', context)


def list_detail(request, list_id):
    if request.method == 'GET':
        current_list = get_object_or_404(TodoList, id=list_id)
        user: CustomUser = request.user
        if user.todolist_set.contains(current_list):
            return render(request, 'frontend/todolist_detail.html', {'list': current_list})
        else:
            return render(request, 'frontend/access_denied.html')

    return render(request, 'frontend/wrong_method.html')


def list_create(request):
    if request.method == 'GET':
        form = TodolistForm
        return render(request, "frontend/list_form_create.html", {"form": form})

    return render(request, 'frontend/wrong_method.html')


def created_successfully(request):
    if request.method == 'GET':
        return render(request, 'frontend/create_successful.html')

    return render(request, 'frontend/wrong_method.html')


def list_edit(request, list_id):
    if request.method == 'GET':
        prev_list = get_object_or_404(TodoList, id=list_id)
        form = TodolistForm(
            {'name': prev_list.name, 'description': prev_list.description, 'tasks': prev_list.tasks.all()})
        return render(request, 'frontend/list_form_edit.html', {"form": form, "list_id": list_id})

    return render(request, 'frontend/wrong_method.html')


def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        return render(request, 'frontend/task_detail.html', {'task': task})

    return render(request, 'frontend/wrong_method.html')


def task_create(request):
    if request.method == 'GET':
        form = TaskForm()
        return render(request, "frontend/task_form_create.html", {"form": form})

    return render(request, 'frontend/wrong_method.html')


def task_edit(request, task_id):
    if request.method == 'GET':
        prev_task = get_object_or_404(Task, id=task_id)
        form = TaskForm({'name': prev_task.name, 'deadline': prev_task.deadline, 'importance': prev_task.importance,
                         'file': prev_task.file, 'image': prev_task.image, 'done': prev_task.done})
        return render(request, 'frontend/task_form_edit.html', {"form": form, "task_id": task_id})

    return render(request, 'frontend/wrong_method.html')


def task_export(request, task_id=None):
    if request.method == 'GET':
        task = get_object_or_404(Task, id=task_id)
        return render(request, 'todolist/task_export.html', {'url': request.build_absolute_uri(),
                                                             'task': task})

    return render(request, 'todolist/wrong_method.html')


def task_import(request, list_id):
    if request.method == 'POST':
        form = TaskImportForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['task_link']
            if UrlDict.objects.filter(key=url).exists():
                original_url = str(UrlDict.objects.get(key=url).original_url)
                matching_url_regex = ('^http://' + request.get_host() + '/' + request.resolver_match.app_name +
                                      '/tasks/' + '(?P<task_id>\\d+)/export/$')
                print(request.resolver_match.app_name)
                p = re.compile(matching_url_regex)
                if p.match(original_url):
                    task_id = int(p.search(original_url).group('task_id'))
                    task = get_object_or_404(Task, pk=task_id)
                    get_object_or_404(List, id=list_id).tasks.add(task)
                    return redirect('todolist:list_detail', list_id=list_id)

            return HttpResponse("Invalid URL")

    elif request.method == 'GET':
        form = TaskImportForm()
        return render(request, 'todolist/task_import.html', {'list_id': list_id, 'form': form})

    return render(request, 'todolist/wrong_method.html')
