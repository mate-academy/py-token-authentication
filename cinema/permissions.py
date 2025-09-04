from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    """
    Permission for Cinema app API endpoints.

    - Admin users: full access (all actions)
    - Authenticated users: read-only access (GET, HEAD, OPTIONS)
    - Anonymous users: no access
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return False
