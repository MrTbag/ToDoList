from django.shortcuts import get_object_or_404

from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from todolist.models import CustomUser, TodoList
from todolist.serializers import TodoListSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def todolist_detail(request, list_id, format=None):
    todolist = get_object_or_404(TodoList, id=list_id)
    user: CustomUser = request.user

    if request.method == 'GET':

        if todolist.owner == user:
            serializer = TodoListSerializer(todolist)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("You do not have permission to access this todolist.", status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':

        if todolist.owner == user:
            serializer = TodoListSerializer(todolist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You do not have permission to edit this todolist.", status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'DELETE':
        if todolist.owner == user:
            todolist.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You do not have permission to delete this todolist.", status=status.HTTP_403_FORBIDDEN)
