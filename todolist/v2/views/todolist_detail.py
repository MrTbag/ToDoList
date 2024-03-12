from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from todolist.models import TodoList
from todolist.v2.serializers import TodoListSerializer


class TodolistDetail(RetrieveUpdateDestroyAPIView):
    queryset = TodoList.objects.all()
    serializer_class = TodoListSerializer
    permission_classes = [IsAuthenticated]

    def check_object_permissions(self, request, obj):
        for _ in self.get_permissions():
            if not request.user == obj.owner:
                self.permission_denied(
                    request,
                    message="You do not have permission to view this list",
                )




