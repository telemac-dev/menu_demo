# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # URLs para projetos
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/reports/', views.ProjectReportsView.as_view(), name='project_reports'),

    # URLs para clientes
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views.ClientCreateView.as_view(), name='client_create'),

    # URLs para administração
    path('admin/users/', views.UserListView.as_view(), name='user_list'),
    path('admin/groups/', views.GroupListView.as_view(), name='group_list'),
    path('admin/settings/', views.SettingsView.as_view(), name='settings'),
]
