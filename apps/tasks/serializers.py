from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    The serializer represents task information.
    """
    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'completed')
        read_only_fields = ['user']

    def save(self, **kwargs):
        return super().save(**kwargs, user=self.context['request'].user)
