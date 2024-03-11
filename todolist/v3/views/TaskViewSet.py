from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from todolist.models import CustomUser

from todolist.v2.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user: CustomUser = self.request.user
        return user.task_set.all()
