from rest_framework import serializers
from todolist.models import Task


class TaskImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['url']
