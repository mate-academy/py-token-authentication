from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_auth_user = bool(
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        )
        is_admin = bool(request.user and request.user.is_staff)
        return is_auth_user or is_admin
