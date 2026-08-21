from rest_framework import permissions
from rest_framework.request import Request


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        return bool(
            (
                request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated
            )
            or request.user.is_staff
        )
