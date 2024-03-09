from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from todolist.models import CustomUser
from todolist.serializers import ListSerializer


@api_view(['GET', 'POST'])
def todolist_list(request, format=None):
    if request.method == 'GET':
        user: CustomUser = request.user
        lists = user.list_set.all()
        serializer = ListSerializer(lists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = ListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)