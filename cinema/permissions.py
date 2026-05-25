from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """Allow full access to admins.

    Authenticated non-admin users get read-only access.
    Unauthenticated users are denied.
    """

    def has_permission(
        self, request: Request, view: APIView
    ) -> bool:
        is_authenticated = bool(request.user and request.user.is_authenticated)
        if request.method in SAFE_METHODS and is_authenticated:
            return True
        return bool(is_authenticated and request.user.is_staff)
