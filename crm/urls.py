from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('clients/<int:client_id>/projects/', views.ProjectCreateView.as_view(), name='create-project'),
    path('projects/', views.UserProjectsView.as_view(), name='user-projects'),
]
