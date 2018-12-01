from rest_framework import serializers
from core.models import Task


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(
        read_only=True, source='created_by.username')
    acceptor = serializers.CharField(
        read_only=True, source="accepted_by.username")

    class Meta:
        model = Task
        fields = (
            "title", "creator", "acceptor", "priority", "state",
            "timeline", "created"
        )