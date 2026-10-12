from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_admin = request.user and request.user.is_staff
        is_authenticated_read_only = (
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        )
        return bool(is_admin or is_authenticated_read_only)
