from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as an admin user,
    or is a read-only for non-admin users request.
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


class IfAuthenticatedCanCreateOder(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in ('GET', 'OPTIONS', 'HEAD', 'POST')
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
