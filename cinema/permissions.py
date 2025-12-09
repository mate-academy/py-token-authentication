from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    - Admin: acesso total.
    - Usuário autenticado: somente leitura.
    - NÃO permitir POST para usuários comuns (somente OrderViewSet lida com isso).
    """

    def has_permission(self, request, view):
        # Admin pode tudo
        if request.user and request.user.is_staff:
            return True

        # Métodos seguros: GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # Para todos os outros métodos (POST/PUT/PATCH/DELETE)
        # o acesso só é liberado no OrderViewSet via regra própria
        return False
