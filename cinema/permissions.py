from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.exceptions import NotAuthenticated


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()

        return bool(
            request.method in SAFE_METHODS
            or request.user.is_staff
        )


class IsAuthenticatedOrCreate(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
        return True
