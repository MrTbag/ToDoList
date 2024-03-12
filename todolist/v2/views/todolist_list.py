from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from todolist.models import List, CustomUser
from todolist.v2.serializers import ListSerializer


class TodolistList(ListCreateAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        user: CustomUser = self.request.user
        return user.list_set.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
