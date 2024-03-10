from todolist.models import List
from rest_framework import serializers
from todolist.models import Task
from django.shortcuts import get_object_or_404


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'name', 'description', 'owner', 'pub_date', 'tasks']
        read_only_fields = ['owner']

    def create(self, validated_data):
        current_list = List.objects.create(name=validated_data['name'], description=validated_data['description'],
                                           owner=self.context['request'].user)
        current_list.tasks.set(validated_data['tasks'])
        return current_list

