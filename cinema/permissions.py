from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return False
