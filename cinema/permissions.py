from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Allow full access to admin (staff) users.
    Allow read-only access to any authenticated user.
    Deny everything else (including anonymous users).
    """

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
