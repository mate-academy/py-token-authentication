from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if getattr(user, "is_staff", False):
            return True
        if request.method in SAFE_METHODS:
            return user and user.is_authenticated
        return False
