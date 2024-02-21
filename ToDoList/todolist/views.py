import time
from unittest import loader

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone

from django.views import generic
from .models import List, Task


# Create your views here.

def index(request):
    lists = List.objects.all()
    context = {
        'lists': lists,
        'user': request.user.username
    }
    return render(request, 'todolist/index.html', context)


def list_detail(request, list_id):
    li = get_object_or_404(List, pk=list_id)
    return render(request, 'todolist/list_detail.html', {'li': li})


def list_delete(request, list_id):
    del_list = get_object_or_404(List, pk=list_id)
    name = del_list.name
    del_list.delete()
    return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'list'})


def list_form(request):
    return render(request, 'todolist/list_form.html')


def list_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        pub_date = timezone.now()
        new_list = List.objects.create(name=name, description=description, pub_date=pub_date)
        new_list.save()
        return redirect('todolist:index')


def list_edit(request, list_id):
    tdl = List.objects.get(id=list_id)
    name = tdl.name
    description = tdl.description
    return render(request, 'todolist/list_form.html', {'name': name, 'description': description})


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'todolist/task_detail.html', {'task': task})


def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    name = task.name
    task.delete()
    return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'task'})


def task_form(request, list_id):
    return render(request, 'todolist/task_form.html', {'list_id': list_id})


def task_create(request, list_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        deadline = request.POST.get('deadline')
        date_added = timezone.now()
        importance = request.POST.get('importance')
        task = Task(name=name, deadline=deadline, date_added=date_added, importance=importance)
        task.save()
        parent_list = get_object_or_404(List, pk=list_id)
        parent_list.tasks.add(task)
        return redirect('todolist:list_detail', list_id=list_id)
