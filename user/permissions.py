from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):

        if request.user and request.user.is_staff:
            return True

        if request.user and request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            if request.method == "POST" and getattr(
                    view, "basename", "") == "orders":
                return True
            return False

        return False
