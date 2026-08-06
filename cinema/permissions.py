from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_authenticated_read_only = (
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        )
        is_admin = request.user and request.user.is_staff

        return bool(is_authenticated_read_only or is_admin)
