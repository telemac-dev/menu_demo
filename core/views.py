# core/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from user_management.models import UserAccessLog  # Adicionar esta importação

# Views simples para demonstração
# core/views.py
@login_required
def dashboard(request):
    """
    Renderiza a página do dashboard com informações personalizadas.
    """
    # Obter atividades recentes do usuário
    recent_activities = UserAccessLog.objects.filter(user=request.user).order_by('-timestamp')[:5]

    # Você pode adicionar outras informações relevantes aqui

    return render(request, 'pages/dashboard.html', {
        'recent_activities': recent_activities,
    })


# Views baseadas em classe para projetos
class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/project_list.html'
    permission_required = 'core.view_project'

class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/project_create.html'
    permission_required = 'core.add_project'

class ProjectReportsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/project_reports.html'
    permission_required = 'core.view_projectreport'

# Views para clientes
class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/client_list.html'
    permission_required = 'core.view_client'

class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/client_create.html'
    permission_required = 'core.add_client'

# Views para administração
class UserListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/user_list.html'
    permission_required = 'auth.view_user'

class GroupListView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/group_list.html'
    permission_required = 'auth.view_group'

class SettingsView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'pages/settings.html'
    permission_required = 'core.change_settings'
