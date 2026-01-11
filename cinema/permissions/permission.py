from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import exceptions


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Admins: full access
    Authenticated non-admins: read-only
    """
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        if request.user.is_authenticated:
            return request.method in SAFE_METHODS
        return False

    def has_object_permission(self, request, view, obj):
        # Admins: full access
        if request.user.is_staff:
            return True
        # Authenticated users: read-only
        if request.user.is_authenticated and request.method in SAFE_METHODS:
            return True
        # Otherwise: return 404 instead of 403
        raise exceptions.NotFound("Object not found or you do not have access")
