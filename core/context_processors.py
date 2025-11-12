# core/context_processors.py
from .menu_config import MENU_ITEMS

def has_permission(user, permission):
    """Verifica se o usuário tem a permissão especificada."""
    if permission is None:
        return True
    if user.is_superuser:
        return True
    return user.has_perm(permission)

def filter_menu_by_permission(menu_items, user):
    """Filtra os itens de menu com base nas permissões do usuário."""
    filtered_items = []

    for item in menu_items:
        # Verifica permissão para o item atual
        if has_permission(user, item.get('permission')):
            item_copy = item.copy()

            # Se tiver submenu, filtra recursivamente
            if 'children' in item_copy:
                children = filter_menu_by_permission(item_copy['children'], user)

                # Só inclui o item pai se tiver pelo menos um filho visível
                if children:
                    item_copy['children'] = children
                    filtered_items.append(item_copy)

            else:
                # Item sem filhos, adiciona diretamente
                filtered_items.append(item_copy)

    return filtered_items

def menu_processor(request):
    """Context processor que adiciona os menus filtrados ao contexto."""
    user = request.user

    if user.is_authenticated:
        menu_items = filter_menu_by_permission(MENU_ITEMS, user)
    else:
        # Para usuários não autenticados, mostrar apenas itens sem permissão
        menu_items = [item for item in MENU_ITEMS if item.get('permission') is None]

    return {
        'menu_items': menu_items
    }
