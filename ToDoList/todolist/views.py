import time
from unittest import loader

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone

from django.views import generic
from .models import List, Task, CustomUser
from .forms import ListForm, TaskForm

from ToDoList import settings

# Create your views here.
User = settings.AUTH_USER_MODEL


def index(request):
    user: CustomUser = request.user
    if user.is_authenticated:
        lists = user.lists.all()
        context = {
            'lists': lists,
            'user': request.user.username
        }
        return render(request, 'todolist/index.html', context)
    else:
        return render(request, 'todolist/error_login.html')


def list_detail(request, list_id):
    li = get_object_or_404(List, id=list_id)
    return render(request, 'todolist/list_detail.html', {'li': li})


def list_delete(request, list_id):
    del_list = get_object_or_404(List, id=list_id)
    name = del_list.name
    del_list.delete()
    return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'list'})


def list_create(request):
    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            pub_date = timezone.now()
            new_list = List.objects.create(name=name, description=description, pub_date=pub_date)
            new_list.tasks.set(form.cleaned_data['tasks'])
            new_list.save()
            user: CustomUser = request.user
            user.lists.add(new_list)
            return redirect('todolist:index')

    else:
        form = ListForm()

    return render(request, "todolist/list_form.html", {"form": form})


def list_edit(request, list_id):
    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            same_list = List.objects.get(pk=list_id)
            same_list.name = form.cleaned_data['name']
            same_list.description = form.cleaned_data['description']
            same_list.tasks.set(form.cleaned_data['tasks'])
            same_list.save()
            return redirect('todolist:list_detail', list_id=list_id)
    else:
        prev_list = List.objects.get(pk=list_id)
        form = ListForm({'name': prev_list.name, 'description': prev_list.description, 'tasks': prev_list.tasks.all()})

    return render(request, 'todolist/list_form2.html', {"form": form, "list_id": list_id})


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'todolist/task_detail.html', {'task': task})


def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    name = task.name
    task.delete()
    return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'task'})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            deadline = form.cleaned_data['deadline']
            importance = form.cleaned_data['importance']
            task = Task(name=name, deadline=deadline, importance=importance, date_added=timezone.now())
            task.save()
            return render(request, 'todolist/create_successful.html')

    else:
        form = TaskForm()

    return render(request, "todolist/task_form.html", {"form": form})


def task_edit(request, task_id):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = Task.objects.get(pk=task_id)
            task.name = form.cleaned_data['name']
            task.deadline = form.cleaned_data['deadline']
            task.importance = form.cleaned_data['importance']
            task.save()
            return redirect('todolist:task_detail', task_id=task_id)

    else:
        prev_task = Task.objects.get(id=task_id)
        form = TaskForm({'name': prev_task.name, 'deadline': prev_task.deadline, 'importance': prev_task.importance})

    return render(request, "todolist/task_form2.html", {"form": form, "task_id": task_id})
