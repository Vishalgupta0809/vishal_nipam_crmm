from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']


class ProjectSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)  # Expecting user IDs
    created_by = serializers.CharField(source='created_by.username', read_only=True)  # Use username

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'created_at', 'created_by']
        read_only_fields = ['created_at', 'created_by']

    def create(self, validated_data):
        users_data = validated_data.pop('users', [])
        # Create the project instance
        project = Project.objects.create(**validated_data)  # created_by will be set automatically
        
        # Assign users to the project using the set() method
        project.users.set(users_data)  # users_data should be a list of IDs

        return project