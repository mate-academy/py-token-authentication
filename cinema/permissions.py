from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Admin pode tudo.
    Autenticado não-admin: somente leitura.
    Anônimo: sem acesso.
    """

    def has_permission(self, request, view):
        user = request.user
        if getattr(user, "is_staff", False):
            return True
        if (
            request.method in SAFE_METHODS
            and getattr(user, "is_authenticated", False)
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
