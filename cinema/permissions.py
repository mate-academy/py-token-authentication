from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS
             and request.user
             and request.user.is_authenticated)
            or (request.user and request.user.is_staff)
        )


class IsAdminOrAuthenticatedCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        if request.user and request.user.is_authenticated:
            return request.method in ["GET", "POST"]

        return False
