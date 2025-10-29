from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_staff:
            return True
        if request.method in SAFE_METHODS and user and user.is_authenticated:
            return True
        return False
