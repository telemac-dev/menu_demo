# user_management/middleware.py
# Middleware para Registro de Acessos de Usuários
from .models import UserAccessLog

class UserAccessMiddleware:
    """
    Middleware para registrar acessos dos usuários.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Código executado para cada requisição antes da view
        response = self.get_response(request)
        # Código executado para cada requisição depois da view

        # Registra apenas para usuários autenticados e não para arquivos estáticos
        if request.user.is_authenticated and not request.path.startswith('/static/'):
            # Não registra acessos repetidos à mesma página em curto período
            UserAccessLog.objects.create(
                user=request.user,
                action='page_view',
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                path=request.path
            )

        return response

    def get_client_ip(self, request):
        """Obtém o endereço IP do cliente."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
