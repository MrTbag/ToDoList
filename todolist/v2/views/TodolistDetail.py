from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from todolist.models import List
from todolist.v2.serializers import ListSerializer


class TodolistDetail(RetrieveUpdateDestroyAPIView):
    queryset = List.objects.all()
    serializer_class = ListSerializer
    permission_classes = [IsAuthenticated]

    def check_object_permissions(self, request, obj):
        for permission in self.get_permissions():
            if not request.user == obj.owner:
                self.permission_denied(
                    request,
                    message="You do not have permission to view this list",
                )




