from django.contrib import admin
from .models import Project, Client, Settings

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'maintenance_mode')

