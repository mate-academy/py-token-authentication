from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - Admins have full access.
    - Authenticated users have read/write access according to SAFE_METHODS.
    - Anonymous users are denied except where views explicitly allow AllowAny.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or (request.user and request.user.is_staff)


class AuthenticationMixin:
    """
    Mixin to apply token authentication and the custom permission globally.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
