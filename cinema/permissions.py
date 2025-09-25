from rest_framework.permissions import BasePermission, SAFE_METHODS

AUTH_METHODS = SAFE_METHODS + ("POST",)
ADMIN_METHODS = AUTH_METHODS + ("PATCH", "PUT",)


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in AUTH_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (
                request.user
                and request.user.is_staff
                and request.method in ADMIN_METHODS
            )
        )
