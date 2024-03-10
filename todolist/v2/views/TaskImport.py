from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from todolist.models import List, Task
from todolist.serializers import TaskImportSerializer
from url_shortener.models import UrlDict


class TaskImport(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, pk, format=None):
        current_list = get_object_or_404(List, pk=pk)
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
