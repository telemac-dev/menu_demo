# core/menu_config.py

MENU_ITEMS = [
    {
        "name": "Dashboard",
        "url": "core:dashboard",
        "icon": "fa-tachometer-alt",
        "permission": None,  # Sem permissão específica (todos podem ver)
    },
    {
        "name": "Projetos",
        "url": "#",  # URL vazia para menus com submenu
        "icon": "fa-project-diagram",
        "permission": "core.view_project",
        "children": [
            {
                "name": "Listar Projetos",
                "url": "core:project_list",
                "permission": "core.view_project",
            },
            {
                "name": "Novo Projeto",
                "url": "core:project_create",
                "permission": "core.add_project",
            },
            {
                "name": "Relatórios",
                "url": "core:project_reports",
                "permission": "core.view_projectreport",
            },
        ],
    },
    {
        "name": "Clientes",
        "url": "#",
        "icon": "fa-users",
        "permission": "core.view_client",
        "children": [
            {
                "name": "Listar Clientes",
                "url": "core:client_list",
                "permission": "core.view_client",
            },
            {
                "name": "Novo Cliente",
                "url": "core:client_create",
                "permission": "core.add_client",
            },
        ],
    },
    {
        "name": "Administração",
        "url": "#",
        "icon": "fa-cogs",
        "permission": "auth.view_user",
        "children": [
            {
                "name": "Usuários",
                "url": "core:user_list",
                "permission": "auth.view_user",
            },
            {
                "name": "Grupos",
                "url": "core:group_list",
                "permission": "auth.view_group",
            },
            {
                "name": "Configurações",
                "url": "core:settings",
                "permission": "core.change_settings",
            },
        ],
    },
]
