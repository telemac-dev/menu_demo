# core/templatetags/menu_tags.py
from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context, url_name):
    """Verifica se a URL atual corresponde à URL do item de menu."""
    request = context['request']
    if url_name == '#':
        return ""

    try:
        pattern = reverse(url_name)
        if pattern == request.path:
            return "active"
        # Para considerar URLs aninhadas como ativas
        elif request.path.startswith(pattern) and pattern != '/':
            return "active"
    except NoReverseMatch:
        return ""

    return ""

@register.filter
def has_children(menu_item):
    """Verifica se um item de menu tem filhos."""
    return 'children' in menu_item and len(menu_item['children']) > 0

@register.inclusion_tag('menu/submenu.html', takes_context=True)
def render_submenu(context, children):
    """Renderiza um submenu recursivamente."""
    return {
        'menu_items': children,
        'request': context['request']
    }
