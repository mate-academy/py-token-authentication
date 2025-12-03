from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    SAFE_METHODS
)


class IsAuthenticatedForMovieSession(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


class IsAdminAllOrIsAuthenticatedForCreateAndRead(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


class IsAdminOrListCreateRetrieve(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


class IsAuthenticatedForOrder(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS + ("POST",):
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)
