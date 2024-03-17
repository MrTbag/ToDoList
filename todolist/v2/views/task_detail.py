from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from todolist.models import Task
from todolist.v2.serializers import TaskSerializer


class TaskDetail(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def check_object_permissions(self, request, obj):
        for _ in self.get_permissions():
            if not request.user == obj.creator:
                self.permission_denied(
                    request,
                    message="You do not have permission to view this task",
                )
