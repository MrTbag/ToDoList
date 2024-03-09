from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import List, Task, CustomUser
from .serializers import ListSerializer, TaskSerializer, TaskImportSerializer

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
            task.url = url
            return Response("Shorten this url and share it with others to be able to import this task.\n" +
                            "URL: " + url + "\n" + "Title: " + task.name, status=status.HTTP_200_OK)
        else:
            return Response("You do not have permission to export this task.", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def task_import(request, list_id, format=None):
    current_list = get_object_or_404(List, pk=list_id)
    user: CustomUser = request.user

    if request.method == 'POST':
        if current_list.owner == user:
            serializer = TaskImportSerializer(data=request.data)
            if serializer.is_valid():
                url = serializer.validated_data['url']

                if not UrlDict.objects.filter(key=url).exists():
                    return Response("Invalid URL", status=status.HTTP_404_NOT_FOUND)

                original_url = get_object_or_404(UrlDict, key=url).original_url
                task = get_object_or_404(Task, url=original_url)

                if not current_list.tasks.contains(task):
                    current_list.tasks.add(task)
                    return Response("Task '" + task.name + "' was imported to list '" + current_list.name + "'",
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response("You already have this task in this list", status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You do not have permission to import this task onto this list.",
                            status=status.HTTP_401_UNAUTHORIZED)

