from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            (request.user and request.user.is_staff) or
            (
                request.method in SAFE_METHODS and
                request.user and request.user.is_authenticated
            )
        )


class IsAdminOrAuthenticatedCreateOrder(BasePermission):
    def has_permission(self, request, view):
        # Allow list if authenticated, create if authenticated, admin has full access
        return (
            (request.user and request.user.is_staff) or
            (
                request.method in ["GET", "POST"] and
                request.user and request.user.is_authenticated
            )
        )
