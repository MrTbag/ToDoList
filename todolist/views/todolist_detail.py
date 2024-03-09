from django.shortcuts import get_object_or_404

from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from todolist.models import CustomUser, List
from todolist.serializers import ListSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def todolist_detail(request, list_id, format=None):
    current_list = get_object_or_404(List, id=list_id)
    user: CustomUser = request.user

    if request.method == 'GET':

        if current_list.owner == user:
            serializer = ListSerializer(current_list)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("You do not have permission to access this todolist.", status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PUT':

        if current_list.owner == user:
            serializer = ListSerializer(current_list, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("You do not have permission to edit this todolist.", status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'DELETE':
        if current_list.owner == user:
            current_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("You do not have permission to delete this todolist.", status=status.HTTP_403_FORBIDDEN)
