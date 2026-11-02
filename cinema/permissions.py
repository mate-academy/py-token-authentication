from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Custom permission to only allow administrators full access and
    authenticated users read-only access.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if (
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ):
            return True
        return False
