from todolist.models import TodoList
from rest_framework import serializers


class TodoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoList
        fields = ['id', 'name', 'description', 'owner', 'pub_date', 'tasks']
        read_only_fields = ['owner']
