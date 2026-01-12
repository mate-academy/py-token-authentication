from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Admin users have full access.
    Authenticated users have read-only access.
    """

    def has_permission(self, request, view):
        # Admin → allow everything
        if request.user and request.user.is_staff:
            return True

        # Authenticated → read-only
        if request.user and request.user.is_authenticated:
            return request.method in SAFE_METHODS

        return False
