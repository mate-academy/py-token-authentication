from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if getattr(view, "basename", None) == "orders":
            return request.user and request.user.is_authenticated

        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
