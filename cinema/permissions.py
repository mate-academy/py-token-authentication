from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - Full access to admin users
    - Read-only access to authenticated users
    - No access to unauthenticated users
    """
    def has_permission(self, request, view):
        return bool(
            (request.user and request.user.is_staff) or
            (request.user and request.user.is_authenticated and request.method in permissions.SAFE_METHODS)
        )
