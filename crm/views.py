from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

# Client List and Create View
class ClientListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Client Detail View: Retrieve, Update, Delete
class ClientDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        client = get_object_or_404(Client, pk=pk)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, client_id):
        # Retrieve the client based on the client_id from the URL
        client = get_object_or_404(Client, id=client_id)

        # Prepare data for the serializer, including the client ID
        project_data = {
            'project_name': request.data.get('project_name'),
            'client': client.id,  # Pass the client ID directly
            'users': [user['id'] for user in request.data.get('users', [])]  # Extract user IDs from 
        }

        # Create the serializer instance
        serializer = ProjectSerializer(data=project_data)
        if serializer.is_valid():
            project = serializer.save(created_by=request.user)  # Save the project and set created_by
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
# List Projects for Logged-in User
class UserProjectsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Fetch projects assigned to the logged-in user
        projects = Project.objects.filter(users=request.user)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
