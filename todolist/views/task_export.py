from django.shortcuts import get_object_or_404

from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from todolist.models import CustomUser, Task


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
