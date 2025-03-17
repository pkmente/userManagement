from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'priority', 'due_date', 'status', 'assignee', 'user']
        read_only_fields = ['user']
