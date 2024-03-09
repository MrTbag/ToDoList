from rest_framework import status

from rest_framework.response import Response
from rest_framework.decorators import api_view

from todolist.models import CustomUser
from todolist.serializers import TaskSerializer


@api_view(['GET', 'POST'])
def task_list(request, format=None):
    user: CustomUser = request.user
    if request.method == 'GET':
        tasks = user.task_set.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

