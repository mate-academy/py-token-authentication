from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The request for admin user to get/update/delete data
    For auth user only to get data
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and request.user
            and request.user.is_authenticated
        ) or (request.user and request.user.is_staff)
