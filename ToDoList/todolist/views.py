import time
from unittest import loader

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.utils import timezone

from django.views import generic
from .models import List, Task
from .forms import ListForm, TaskForm


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


def list_create(request):
    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            name = request.POST.get('name')
            description = request.POST.get('description')
            pub_date = timezone.now()
            tasks = request.POST.get('tasks')
            print(form.cleaned_data['tasks'])
            new_list = List.objects.create(name=name, description=description, pub_date=pub_date)
            new_list.tasks.set(form.cleaned_data['tasks'])
            new_list.save()
            return redirect('todolist:index')

    else:
        form = ListForm()

    return render(request, "todolist/list_form.html", {"form": form})


def list_edit(request, list_id):
    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            name = request.POST.get('name')
            description = request.POST.get('description')
            pub_date = timezone.now()
            same_list = List.objects.get(list_id=list_id)
            same_list.update(name=name, description=description, pub_date=pub_date)
            return redirect('todolist:index')
    else:
        form = ListForm(instance=get_object_or_404(List, pk=list_id))

    return render(request, 'todolist/list_form2.html', {"form": form, "list_id": list_id})


def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    return render(request, 'todolist/task_detail.html', {'task': task})


def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    name = task.name
    task.delete()
    return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'task'})


def task_form(request):
    form = TaskForm(request.POST)
    return render(request, 'todolist/task_form.html', {'form': form})


def task_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        deadline = request.POST.get('deadline')
        date_added = timezone.now()
        importance = request.POST.get('importance')
        task = Task(name=name, deadline=deadline, date_added=date_added, importance=importance)
        task.save()
        print(task.id)
        return render(request, 'todolist/create_successful.html')


def task_edit(request, task_id):
    form = TaskForm(instance=get_object_or_404(Task, pk=task_id))
    return render(request, 'todolist/task_form.html', context={'form': form})
