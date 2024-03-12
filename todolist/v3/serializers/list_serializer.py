from todolist.models import List
from rest_framework import serializers


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name', 'description', 'owner', 'pub_date', 'tasks']
        read_only_fields = ['owner']

    def validate_tasks(self, value):
        for task in value:
            if task.creator != self.context['request'].user:
                raise serializers.ValidationError("You do not have permission to add tasks you do not own")
        return value
