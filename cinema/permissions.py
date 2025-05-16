from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        elif request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
