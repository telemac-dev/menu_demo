# user_management/models.py
# Modelos para Perfil e Histórico de Acesso de Usuários
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """
    Modelo para armazenar informações adicionais do usuário.
    Estende o modelo User padrão do Django.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    last_password_change = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class UserAccessLog(models.Model):
    """
    Modelo para registrar o histórico de acesso dos usuários.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50)  # login, logout, etc.
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    path = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

# Sinais para criar automaticamente um perfil quando um usuário é criado
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
