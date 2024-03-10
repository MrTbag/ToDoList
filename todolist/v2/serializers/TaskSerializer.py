from rest_framework import serializers
from todolist.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'importance', 'deadline', 'creator', 'file', 'image', 'date_added']
        extra_kwargs = {
            'creator': {'read_only': True},
        }

    def create(self, validated_data):
        task = Task.objects.create(name=validated_data['name'], importance=validated_data['importance'],
                                   file=validated_data['file'], image=validated_data['image'],
                                   creator=self.context['user'], deadline=validated_data['deadline'])
        return task
