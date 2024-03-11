from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from todolist.v2.serializers import ListSerializer

from todolist.models import CustomUser


class TodolistViewSet(ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user: CustomUser = self.request.user
        return user.list_set.all()
