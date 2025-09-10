from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminAllORIsAuthenticatedOrReadOnly(
    BasePermission
):
    """
    The request is authenticated as an admin -
    read/write, if a user - read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or (request.user and request.user.is_staff)
