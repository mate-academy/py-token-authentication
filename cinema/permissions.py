from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    Permission that allows:
    - Administrators to perform read, create, update, delete
    - Authenticated users only have secure GET, HEAD, OPTIONS methods.
    - Access to unauthenticated users is completely denied.
    """

    def has_permission(self, request, view):
        return bool(
            (request.method in SAFE_METHODS
             and request.user
             and request.user.is_authenticated)
            or (request.user
                and request.user.is_staff)
        )
