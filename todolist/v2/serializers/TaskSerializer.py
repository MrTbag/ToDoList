from rest_framework import serializers
from todolist.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'importance', 'deadline', 'creator', 'file', 'image', 'date_added', 'done']
        extra_kwargs = {
            'creator': {'read_only': True},
        }
