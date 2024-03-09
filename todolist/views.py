import re
import io

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import permissions, viewsets, generics, authentication, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

from .models import List, Task, CustomUser
from .forms import ListForm, TaskForm, TaskImportForm
from .serializers import ListSerializer, TaskSerializer

from url_shortener.models import UrlDict


@api_view(['GET', 'POST'])
def todolist_list(request, format=None):
    if request.method == 'GET':
        user: CustomUser = request.user
        lists = user.list_set.all()
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def todolist_detail(request, list_id, format=None):
    current_list = get_object_or_404(List, id=list_id)
    user: CustomUser = request.user

    if request.method == 'GET':

        if current_list.owner == user:
            serializer = ListSerializer(current_list)
            return Response(serializer.data)
        else:
            return Response("You do not have permission to access this data.", status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':

        if current_list.owner == user:
            serializer = ListSerializer(current_list, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        current_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
