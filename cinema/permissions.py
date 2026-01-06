from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.user
                and request.user.is_authenticated
                and request.method in SAFE_METHODS
            )
            or (request.user and request.user.is_staff)
        )
