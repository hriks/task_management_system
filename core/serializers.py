from rest_framework import serializers
from core.models import Task, Notifications


class TaskSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(
        read_only=True, source='created_by.username')
    acceptor = serializers.CharField(
        read_only=True, source="accepted_by.username")
    created = serializers.DateTimeField(format="%d/%m/%Y %H:%M %p")

    class Meta:
        model = Task
        fields = (
            "title", "description", "creator", "acceptor", "priority", "state",
            "timeline", "created", "id"
        )


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notifications
        fields = "__all__"
