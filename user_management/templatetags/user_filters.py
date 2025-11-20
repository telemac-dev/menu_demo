# user_management/templatetags/user_filters.py
from django import template

register = template.Library()

@register.filter
def has_profile(user):
    """Verifica se um usuário tem perfil."""
    try:
        return bool(user.profile)
    except:
        return False

@register.filter
def get_profile_image(user):
    """Retorna a URL da imagem do perfil do usuário se existir."""
    try:
        if user.profile and user.profile.profile_image:
            return user.profile.profile_image.url
        return None
    except:
        return None
