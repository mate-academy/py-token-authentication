from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if (request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated):
            return True
        return False
