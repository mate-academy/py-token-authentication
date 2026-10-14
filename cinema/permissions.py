from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if request.method in SAFE_METHODS:
            return bool(user and user.is_authenticated)

        return bool(user and user.is_staff)