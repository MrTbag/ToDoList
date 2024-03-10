from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from todolist.models import Task


class TaskExport(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk, format=None):
        task = get_object_or_404(Task, id=pk)
        url = request.build_absolute_uri()
        task.url = url
        return Response("Shorten this url and share it with others to be able to import this task.\n " +
                        "URL: " + url + " \n" + "Title: " + task.name, status=status.HTTP_200_OK)

