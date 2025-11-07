from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            and request.user.is_authenticated
            and request.user
        ) or (
            request.user
            and request.user.is_staff
        )
