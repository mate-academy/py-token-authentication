from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS
             and request.user
             and request.user.is_authenticated)
            or (request.user and request.user.is_staff)
        )


class IsAdminOrIfAuthenticatedCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.is_authenticated:
            return request.method in SAFE_METHODS or request.method == "POST"
        return False
