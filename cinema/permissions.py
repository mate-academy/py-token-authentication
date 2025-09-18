from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        if getattr(view, "basename", None) == "order" and request.method == "POST":
            return request.user and request.user.is_authenticated
        return False
