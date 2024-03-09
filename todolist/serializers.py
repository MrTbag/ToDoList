from .models import List, Task, CustomUser
from rest_framework import serializers


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class TaskImportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['url']
