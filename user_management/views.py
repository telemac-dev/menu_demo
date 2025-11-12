# user_management/views.py
# Views para Gestão de Usuários
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction

from .forms import UserRegistrationForm, UserProfileForm, UserPermissionForm
from .models import UserAccessLog

def register_view(request):
    """
    View para registro de novos usuários.
    """
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Registra o evento de registro
            UserAccessLog.objects.create(
                user=user,
                action='register',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            # Autentica o usuário após o registro
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, 'Conta criada com sucesso!')
            return redirect('core:dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'user_management/register.html', {'form': form})

@login_required
def profile_view(request):
    """
    View para visualização e edição do perfil do usuário.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('user_management:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)

    # Obtém o histórico de acesso do usuário
    access_logs = UserAccessLog.objects.filter(user=request.user).order_by('-timestamp')[:10]

    return render(request, 'user_management/profile.html', {
        'form': form,
        'access_logs': access_logs
    })

@login_required
def change_password_view(request):
    """
    View para alteração de senha.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()

            # Atualiza a data da última alteração de senha
            user.profile.last_password_change = timezone.now()
            user.profile.save()

            # Registra o evento de alteração de senha
            UserAccessLog.objects.create(
                user=user,
                action='password_change',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )

            # Mantém o usuário logado após a alteração de senha
            update_session_auth_hash(request, user)

            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('user_management:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user_management/password_change.html', {'form': form})

@login_required
def access_history_view(request):
    """
    View para visualização do histórico de acesso completo.
    """
    access_logs = UserAccessLog.objects.filter(user=request.user).order_by('-timestamp')

    return render(request, 'user_management/access_history.html', {
        'access_logs': access_logs
    })

# Views para administração de usuários

class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    View para listar todos os usuários (apenas para administradores).
    """
    model = User
    template_name = 'user_management/admin/user_list.html'
    context_object_name = 'users'
    permission_required = 'auth.view_user'

    def get_queryset(self):
        return User.objects.all().order_by('username')

@login_required
@permission_required('auth.change_user')
def user_permissions_view(request, user_id):
    """
    View para gerenciar permissões de um usuário específico.
    """
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserPermissionForm(request.POST, user=user)
        if form.is_valid():
            with transaction.atomic():
                form.save()

            messages.success(request, f'Permissões do usuário {user.username} atualizadas com sucesso!')
            return redirect('user_management:user_list')
    else:
        form = UserPermissionForm(user=user)

    return render(request, 'user_management/admin/user_permissions.html', {
        'form': form,
        'managed_user': user
    })
