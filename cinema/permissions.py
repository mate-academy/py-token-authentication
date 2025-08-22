from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated)
            or (
                request.user and request.user.is_staff
            )
        )


class NoDeleteUpdatePermission(IsAdminOrIfAuthenticatedReadOnly):
    def has_permission(self, request, view):
        if request.method in ("DELETE", "PUT", "PATCH"):
            return False
        return super().has_permission(request, view)


class OrderPermission(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
