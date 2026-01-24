from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    """
    Permissão customizada:
    - Admins têm acesso total (exceto onde o ViewSet o restringe).
    - Usuários autenticados têm permissão de leitura (GET, HEAD, OPTIONS).
    - Usuários anônimos têm permissão de leitura (GET, HEAD, OPTIONS) onde o ViewSet permitir.
    """

    def has_permission(self, request, view):
        # Permitir acesso se for requisição de leitura (List/Retrieve)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permitir requisições de escrita (POST, PUT, PATCH, DELETE) apenas para Staff (Admin)
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # Para requisições de escrita em objetos específicos:
        if request.method in permissions.SAFE_METHODS:
            return True

        # Se o usuário for staff, ele pode fazer o que o ViewSet permitir (já controlado pelo has_permission/actions)
        if request.user and request.user.is_staff:
            return True

        # Usuários normais autenticados (não-staff) são restritos pelas ações definidas no ViewSet
        # e pela regra geral de is_staff acima. Para escritas não-staff, será False,
        # exceto em casos muito específicos (como o OrderViewSet onde validaremos a autoria no View).
        return False
