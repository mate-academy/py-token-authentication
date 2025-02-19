# permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Custom permission:
    - Admin users can perform any action.
    - Authenticated non-admin users can only perform safe (read-only) actions.
    """
    def has_permission(self, request, view):
        # Allow full access if user is admin.
        if request.user and request.user.is_staff:
            return True

        # Otherwise, if the user is authenticated, only allow safe methods.
        if request.user and request.user.is_authenticated:
            return request.method in SAFE_METHODS

        # Otherwise, deny access.
        return False
