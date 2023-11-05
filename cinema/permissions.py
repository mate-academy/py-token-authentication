from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (
                    request.method in ("GET", "PUT", "HEAD", "OPTIONS")
                    and request.user
                    and request.user.is_staff
            )
        )
