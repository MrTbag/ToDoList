from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from todolist.models import CustomUser, Task

from todolist.v2.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user: CustomUser = self.request.user
        return user.task_set.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        task: Task = self.get_object()
        url = request.build_absolute_uri()
        task.url = url
        task.save()
        return Response("Shorten this url and share it with others to be able to import this task.\n " +
                        "URL: " + url + " \n" + "Title: " + task.name, status=status.HTTP_200_OK)


