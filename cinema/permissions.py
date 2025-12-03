from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Custom permission:
    - Admin users have full access
    - Authenticated users have read-only access
    - Unauthenticated users have no access
    """
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.method in SAFE_METHODS
                or request.user.is_staff
            )
        )
