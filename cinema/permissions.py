from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Admins have full access.
    - Authenticated users have read access according to SAFE_METHODS.
    - Anonymous users are denied access
    (authentication required for all requests).
    - Non-safe methods (POST, PUT, PATCH, DELETE) require staff authentication.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.is_authenticated:
            return request.method in permissions.SAFE_METHODS
        return False


class AuthenticationMixin:
    """
    Mixin to apply token authentication and the custom permission by default.

    This mixin ensures that all cinema endpoints use:
    - TokenAuthentication for authentication
    - IsAdminOrIfAuthenticatedReadOnly for permissions

    All cinema viewsets inherit this mixin to apply consistent authentication
    and permission logic across the cinema app.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
