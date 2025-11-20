# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from user_management.models import UserAccessLog
from .models import Project, Client, Settings

# Views simples para demonstração
@login_required
def dashboard(request):
    """
    Renderiza a página do dashboard com informações personalizadas.
    """
    # Obter atividades recentes do usuário
    recent_activities = UserAccessLog.objects.filter(user=request.user).order_by('-timestamp')[:5]

    # Contagens para o dashboard
    project_count = Project.objects.count()
    client_count = Client.objects.count()
    user_count = User.objects.count()

    return render(request, 'pages/dashboard.html', {
        'recent_activities': recent_activities,
        'project_count': project_count,
        'client_count': client_count,
        'user_count': user_count,
    })


# Views baseadas em classe para projetos
class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Project
    template_name = 'pages/project_list.html'
    context_object_name = 'projects'
    permission_required = 'core.view_project'

class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Project
    template_name = 'pages/project_create.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('core:project_list')
    permission_required = 'core.add_project'

class ProjectReportsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/project_reports.html'
    permission_required = 'core.view_projectreport'

# Views para clientes
class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    template_name = 'pages/client_list.html'
    context_object_name = 'clients'
    permission_required = 'core.view_client'

class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    template_name = 'pages/client_create.html'
    fields = ['name', 'email', 'phone']
    success_url = reverse_lazy('core:client_list')
    permission_required = 'core.add_client'

# Views para administração
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'pages/user_list.html'
    context_object_name = 'users'
    permission_required = 'auth.view_user'

class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Group
    template_name = 'pages/group_list.html'
    context_object_name = 'groups'
    permission_required = 'auth.view_group'

class SettingsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/settings.html'
    permission_required = 'core.change_settings'
