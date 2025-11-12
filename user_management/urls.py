# user_management/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user_management'

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(
        template_name='user_management/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Registro e perfil
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/password/', views.change_password_view, name='change_password'),
    path('profile/history/', views.access_history_view, name='access_history'),

    # Administração de usuários
    path('admin/users/', views.UserListView.as_view(), name='user_list'),
    path('admin/users/<int:user_id>/permissions/', views.user_permissions_view, name='user_permissions'),
]
