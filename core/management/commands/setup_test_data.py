# core/management/commands/setup_test_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Project, Client, Settings

class Command(BaseCommand):
    help = 'Configura dados de teste para demonstração de menus dinâmicos'

    def handle(self, *args, **options):
        # Criar grupos
        admin_group, _ = Group.objects.get_or_create(name='Administradores')
        project_manager_group, _ = Group.objects.get_or_create(name='Gerentes de Projetos')
        client_manager_group, _ = Group.objects.get_or_create(name='Gerentes de Clientes')

        # Obter content types
        project_ct = ContentType.objects.get_for_model(Project)
        client_ct = ContentType.objects.get_for_model(Client)
        settings_ct = ContentType.objects.get_for_model(Settings)

        # Adicionar permissões aos grupos
        # Administradores têm acesso completo
        admin_perms = Permission.objects.all()
        admin_group.permissions.set(admin_perms)

        # Gerentes de Projetos podem gerenciar projetos
        project_perms = Permission.objects.filter(content_type=project_ct)
        project_manager_group.permissions.set(project_perms)

        # Gerentes de Clientes podem gerenciar clientes
        client_perms = Permission.objects.filter(content_type=client_ct)
        client_manager_group.permissions.set(client_perms)

        # Criar usuários de teste
        # Admin
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'is_staff': True}
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            admin_user.groups.add(admin_group)

        # Gerente de Projetos
        pm_user, created = User.objects.get_or_create(
            username='projeto',
            defaults={'email': 'projeto@example.com'}
        )
        if created:
            pm_user.set_password('projeto123')
            pm_user.save()
            pm_user.groups.add(project_manager_group)

        # Gerente de Clientes
        cm_user, created = User.objects.get_or_create(
            username='cliente',
            defaults={'email': 'cliente@example.com'}
        )
        if created:
            cm_user.set_password('cliente123')
            cm_user.save()
            cm_user.groups.add(client_manager_group)

        self.stdout.write(self.style.SUCCESS('Dados de teste configurados com sucesso!'))
