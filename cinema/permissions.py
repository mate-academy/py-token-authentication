from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Global permission for cinema app
    anonymous users should not be allowed to read data
    regular users should not be allowed to manipulate data,
    besides their orders
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or bool(
            request.user
            and request.user.is_staff
        )
