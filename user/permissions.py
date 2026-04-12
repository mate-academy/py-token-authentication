from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """Read-only for authenticated users, write for admins."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.method in SAFE_METHODS
                or request.user.is_staff
            )
        )


class IsAdminAllORIsAuthenticatedReadOnly(
    IsAdminOrIfAuthenticatedReadOnly
):
    pass
