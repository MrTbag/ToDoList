from django.shortcuts import get_object_or_404

from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from todolist.models import CustomUser, Task
from todolist.serializers import TaskSerializer


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
