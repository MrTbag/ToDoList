from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from todolist.serializers import TaskImportSerializer
from todolist.v3.serializers import TodoListSerializer

from todolist.models import CustomUser, Task, TodoList
from url_shortener.models import UrlDict


class TodolistViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'import_task':
            return TaskImportSerializer
        else:
            return TodoListSerializer

    def get_queryset(self):
        user: CustomUser = self.request.user
        return user.todolist_set.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

    def perform_create(self, serializer):
        tasks = serializer.validated_data['tasks']
        for task in tasks:
            if task.creator != self.request.user:
                raise PermissionDenied
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        tasks = serializer.validated_data['tasks']
        for task in tasks:
            if task.creator != self.request.user and not self.get_object().tasks.filter(id=task.id).exists():
                raise PermissionDenied
        serializer.save()

    @action(detail=True, methods=['post'])
    def import_task(self, request, pk=None):
        current_list = get_object_or_404(TodoList, pk=pk)
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
