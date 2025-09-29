from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    - Admin: full access
    - Authenticated: read-only
    - Unauthenticated: no access
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.is_authenticated:
            return request.method in SAFE_METHODS
        return False


class IsAuthenticatedAndOrderOnly(BasePermission):
    """
    Allows only authorized users to create and view orders.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
