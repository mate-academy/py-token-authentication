from rest_framework.permissions import (BasePermission,
                                        SAFE_METHODS)


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as an admin - read/write,
    if as user - read-only request.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True

        return False


class IsAuthenticatedOrAdminReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_staff:
            return True
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        if request.method == "POST" and request.user.is_authenticated:
            return True
        return False
