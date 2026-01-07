from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as an admin — read/write.
    If authenticated user — read only.
    """

    def has_permission(self, request, view):
        is_readonly = request.method in SAFE_METHODS and (
            request.user
            and request.user.is_authenticated
        )

        is_admin = request.user and request.user.is_staff

        return bool(is_readonly or is_admin)
