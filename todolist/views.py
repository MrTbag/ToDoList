import re
import io

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import permissions, viewsets, generics, authentication, status
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
        return Response(serializer.data, status=status.HTTP_200_OK)

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
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("You do not have permission to access this todolist.", status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':

        if current_list.owner == user:
            serializer = ListSerializer(current_list, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You do not have permission to edit this todolist.", status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'DELETE':
        if current_list.owner == user:
            current_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You do not have permission to delete this todolist.", status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'POST'])
def task_list(request, format=None):
    user: CustomUser = request.user
    if request.method == 'GET':
        tasks = user.task_set.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, task_id, format=None):
    task = get_object_or_404(Task, pk=task_id)
    user: CustomUser = request.user
    if request.method == 'GET':
        if task.creator == user:
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("You do not have permission to access this task.", status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        if task.creator == user:
            serializer = TaskSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You do not have permission to edit this task.", status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'DELETE':
        if task.creator == user:
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You do not have permission to delete this task.", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def task_export(request, task_id, format=None):
    task = get_object_or_404(Task, id=task_id)
    user: CustomUser = request.user

    if request.method == 'GET':
        if task.creator == user:
            url = request.build_absolute_uri()
            return Response("Shorten this url and share it with others to be able to import this task.\n" +
                            "URL: " + url + "\n" + "Title: " + task.name, status=status.HTTP_200_OK)
        else:
            return Response("You do not have permission to export this task.", status=status.HTTP_401_UNAUTHORIZED)


def task_import(request, list_id):
    current_list = get_object_or_404(List, pk=list_id)
    user: CustomUser = request.user
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
