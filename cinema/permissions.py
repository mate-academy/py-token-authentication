from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as an admin - read/write,
    if as a user - read only request.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsAuthenticatedOrAdminForOrders(BasePermission):
    """
    Admin -> full access
    Authenticated user -> list and create
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.is_authenticated:
            action = getattr(view, "action", None)  # захист від None
            if action in ["list", "create"]:
                return True

        return False
