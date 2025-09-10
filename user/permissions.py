from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        else:
            return (request.method in permissions.SAFE_METHODS
                    and request.user and request.user.is_authenticated)
