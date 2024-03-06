import re

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import List, Task, CustomUser, IntermediaryListTask
from .forms import ListForm, TaskForm, TaskImportForm

from url_shortener.models import UrlDict


def index(request):
    if request.method == 'GET':
        user: CustomUser = request.user
        lists = user.list_set.all()
        context = {
            'lists': lists,
            'user': request.user.username
        }
        return render(request, 'todolist/index.html', context)

    return render(request, 'todolist/wrong_method.html')


def list_detail(request, list_id):
    if request.method == 'GET':
        current_list = get_object_or_404(List, id=list_id)
        user: CustomUser = request.user
        if user.list_set.contains(current_list):
            return render(request, 'todolist/list_detail.html', {'list': current_list})
        else:
            return render(request, 'todolist/access_denied.html')

    return render(request, 'todolist/wrong_method.html')


def list_delete(request, list_id):
    if request.method == 'POST':
        user: CustomUser = request.user
        del_list = get_object_or_404(List, id=list_id)
        if user.list_set.contains(del_list):
            name = del_list.name
            del_list.delete()
            return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'list'})
        else:
            return render(request, 'todolist/access_denied.html')
    return render(request, 'todolist/wrong_method.html')


def list_create(request):
    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            user: CustomUser = request.user
            new_list = List.objects.create(name=name, description=description, owner=user)
            new_list.tasks.set(form.cleaned_data['tasks'])
            new_list.save()
            return redirect('todolist:index')

    elif request.method == 'GET':
        form = ListForm()
        return render(request, "todolist/list_form_create.html", {"form": form})

    return render(request, 'todolist/wrong_method.html')


def list_edit(request, list_id):
    user: CustomUser = request.user
    current_list = get_object_or_404(List, id=list_id)
    if user.list_set.contains(current_list):
        if request.method == 'POST':
            form = ListForm(request.POST)

            if form.is_valid():
                current_list.name = form.cleaned_data['name']
                current_list.description = form.cleaned_data['description']
                current_list.tasks.set(form.cleaned_data['tasks'])
                current_list.save()
                return redirect('todolist:list_detail', list_id=list_id)

        elif request.method == 'GET':
            prev_list = get_object_or_404(List, id=list_id)
            form = ListForm(
                {'name': prev_list.name, 'description': prev_list.description, 'tasks': prev_list.tasks.all()})
            return render(request, 'todolist/list_form_edit.html', {"form": form, "list_id": list_id})

        return render(request, 'todolist/wrong_method.html')

    else:
        return render(request, 'todolist/access_denied.html')


def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        return render(request, 'todolist/task_detail.html', {'task': task})

    return render(request, 'todolist/wrong_method.html')


def task_delete(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id)
        name = task.name
        task.delete()
        return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'task'})
    return render(request, 'todolist/wrong_method.html')


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            deadline = form.cleaned_data['deadline']
            importance = form.cleaned_data['importance']
            done = form.cleaned_data['done']
            file = request.FILES.get('file', None)
            image = request.FILES.get('image', None)
            task = Task(name=name, deadline=deadline, importance=importance, file=file,
                        image=image, done=done, creator=request.user)
            task.save()

            return render(request, 'todolist/create_successful.html')

    elif request.method == 'GET':
        form = TaskForm()
        return render(request, "todolist/task_form_create.html", {"form": form})

    return render(request, 'todolist/wrong_method.html')


def task_edit(request, task_id):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid():
            task = get_object_or_404(Task, id=task_id)
            task.name = form.cleaned_data['name']
            task.deadline = form.cleaned_data['deadline']
            task.importance = form.cleaned_data['importance']
            task.file = request.FILES.get('file', None)
            task.image = request.FILES.get('image', None)
            task.done = form.cleaned_data['done']
            task.save()
            return redirect('todolist:task_detail', task_id=task_id)

    elif request.method == 'GET':
        prev_task = get_object_or_404(Task, id=task_id)
        form = TaskForm({'name': prev_task.name, 'deadline': prev_task.deadline, 'importance': prev_task.importance,
                         'file': prev_task.file, 'image': prev_task.image, 'done': prev_task.done})
        return render(request, "todolist/task_form_edit.html", {"form": form, "task_id": task_id})

    return render(request, 'todolist/wrong_method.html')


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
