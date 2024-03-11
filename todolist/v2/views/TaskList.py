from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from todolist.models import Task, CustomUser
from todolist.v2.serializers import TaskSerializer


class TaskList(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user: CustomUser = self.request.user
        return user.task_set.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["user"] = self.request.user
        return context

    # TODO perform create instead of serializer editing

