from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user and request.user.is_authenticated:
            return (
                request.method in permissions.SAFE_METHODS
            ) or request.user.is_staff
        return False


class CreateIfAuthenticated(BasePermission):
    def has_permission(self, request, view) -> bool:
        return bool(
            request.method == "POST"
            and request.user
            and request.user.is_authenticated
        )
