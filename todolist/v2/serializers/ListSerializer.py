from todolist.models import List, CustomUser
from todolist.models import Task
from rest_framework import serializers


class TaskListingField(serializers.RelatedField):
    class Meta:
        model = Task

    def get_queryset(self):
        user: CustomUser = self.context['request'].user
        return user.task_set.all()

    def to_representation(self, value):
        if isinstance(value, Task):
            return value.name
        else:
            raise Exception("This type of object is not supported")


class ListSerializer(serializers.ModelSerializer):
    tasks = TaskListingField(many=True)

    class Meta:
        model = List
        fields = ['id', 'name', 'description', 'owner', 'pub_date', 'tasks']
        read_only_fields = ['owner']

    def create(self, validated_data):
        current_list = List.objects.create(name=validated_data['name'], description=validated_data['description'],
                                           owner=self.context['request'].user)
        current_list.tasks.set(validated_data['tasks'])
        return current_list

    def validate_tasks(self, value):
        for task in value:
            if task.creator != self.context['request'].user:
                raise serializers.ValidationError("You do not have permission to add tasks you do not own")
        return value
