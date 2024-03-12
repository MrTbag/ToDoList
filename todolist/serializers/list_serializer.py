from todolist.models import List
from rest_framework import serializers


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = '__all__'

    def validate_tasks(self, value):
        for task in value:
            if task.creator != self.context['request'].user:
                raise serializers.ValidationError("You do not have permission to add tasks you do not own")
        return value
