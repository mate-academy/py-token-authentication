from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_admin = bool(request.user and request.user.is_staff)
        is_auth = bool(request.user and request.user.is_authenticated)

        return (request.method in SAFE_METHODS and is_auth) or is_admin
