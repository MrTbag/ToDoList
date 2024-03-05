import re

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import List, Task, CustomUser, Hash
from .forms import ListForm, TaskForm, TaskImportForm
from .decorators import authorize


# middleware

@authorize
def index(request):
    if request.method == 'GET':
        user: CustomUser = request.user
        lists = user.lists.all()
        context = {
            'lists': lists,
            'user': request.user.username
        }
        return render(request, 'todolist/index.html', context)

    return render(request, 'todolist/wrong_method.html')


@authorize
def list_detail(request, list_id):
    # check the owner
    if request.method == 'GET':
        current_list = get_object_or_404(List, id=list_id)  # change the name
        return render(request, 'todolist/list_detail.html', {'list': current_list})

    return render(request, 'todolist/wrong_method.html')


@authorize
def list_delete(request, list_id):
    # Check if method is DELETE
    del_list = get_object_or_404(List, id=list_id)
    name = del_list.name
    del_list.delete()
    return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'list'})


@authorize
def list_create(request):
    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            new_list = List.objects.create(name=name, description=description)
            new_list.tasks.set(form.cleaned_data['tasks'])
            new_list.save()
            user: CustomUser = request.user
            user.lists.add(new_list)
            return redirect('todolist:index')

    elif request.method == 'GET':
        form = ListForm()
        return render(request, "todolist/list_form.html", {"form": form})

    return render(request, 'todolist/wrong_method.html')


@authorize
def list_edit(request, list_id):
    if request.method == 'POST':
        form = ListForm(request.POST)

        if form.is_valid():
            same_list = get_object_or_404(List, id=list_id)
            same_list.name = form.cleaned_data['name']
            same_list.description = form.cleaned_data['description']
            same_list.tasks.set(form.cleaned_data['tasks'])
            same_list.save()
            return redirect('todolist:list_detail', list_id=list_id)

    elif request.method == 'GET':
        prev_list = get_object_or_404(List, id=list_id)
        form = ListForm({'name': prev_list.name, 'description': prev_list.description, 'tasks': prev_list.tasks.all()})
        return render(request, 'todolist/list_form2.html', {"form": form, "list_id": list_id})

    return render(request, 'todolist/wrong_method.html')


def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        return render(request, 'todolist/task_detail.html', {'task': task})

    return render(request, 'todolist/wrong_method.html')


@authorize
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    name = task.name
    task.delete()
    return render(request, 'todolist/delete_successful.html', {'name': name, 'item': 'task'})


@authorize
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid():
            name = form.cleaned_data['name']
            deadline = form.cleaned_data['deadline']
            importance = form.cleaned_data['importance']
            # TODO: double check client being able to send no files/images
            # request.FILES.get('file', None)
            file = request.FILES['file']
            image = request.FILES['image']
            task = Task(name=name, deadline=deadline, importance=importance, file=file,
                        image=image)
            task.save()
            return render(request, 'todolist/create_successful.html')

    elif request.method == 'GET':
        form = TaskForm()
        return render(request, "todolist/task_form.html", {"form": form})

    return render(request, 'todolist/wrong_method.html')


@authorize
def task_edit(request, task_id):
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)

        if form.is_valid():
            task = get_object_or_404(Task, id=task_id)
            task.name = form.cleaned_data['name']
            task.deadline = form.cleaned_data['deadline']
            task.importance = form.cleaned_data['importance']
            task.file = request.FILES['file']
            task.image = form.cleaned_data['image']
            task.save()
            return redirect('todolist:task_detail', task_id=task_id)

    elif request.method == 'GET':
        prev_task = get_object_or_404(Task, id=task_id)
        # doesn't pre-populate with file/image
        form = TaskForm({'name': prev_task.name, 'deadline': prev_task.deadline, 'importance': prev_task.importance,
                         'file': prev_task.file, 'image': prev_task.image})
        return render(request, "todolist/task_form2.html", {"form": form, "task_id": task_id})

    return render(request, 'todolist/wrong_method.html')


@authorize
def task_export(request, task_id):
    if request.method == 'GET':
        url = request.build_absolute_uri()

        if not Hash.objects.filter(long_url=url).exists():
            hashed = str(abs(hash(url)))[:10]
            new_hash = Hash(hashed=hashed, long_url=url)
            new_hash.save()

        else:
            hashed = Hash.objects.get(long_url=url).hashed

        begin = 'http://shrtn.link/'
        return render(request, 'todolist/task_export.html',
                      {'task': get_object_or_404(Task, pk=task_id), 'url': begin + hashed + '/'})\

    return render(request, 'todolist/wrong_method.html')


# import: check if he has the task from beforehand. update: it is
@authorize
def task_import(request, list_id):
    if request.method == 'POST':
        form = TaskImportForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['task_link']
            matching_url_regex = '^http://shrtn.link/(?P<hashed>\\d+)/$'
            p = re.compile(matching_url_regex)
            if p.match(url):
                long_url = str(Hash.objects.get(hashed=p.search(url).group('hashed')).long_url)
                matching_url_regex = '^http://127.0.0.1:8000/todolist/tasks/(?P<task_id>\\d+)/export/$'
                p = re.compile(matching_url_regex)
                if p.match(long_url):
                    task_id = int(p.search(long_url).group('task_id'))
                    task = get_object_or_404(Task, pk=task_id)
                    List.objects.get(id=list_id).tasks.add(task)
                    return redirect('todolist:list_detail', list_id=list_id)

            return HttpResponse("Invalid URL")

    elif request.method == 'GET':
        form = TaskImportForm()
        return render(request, 'todolist/task_import.html', {'list_id': list_id, 'form': form})

    return render(request, 'todolist/wrong_method.html')
