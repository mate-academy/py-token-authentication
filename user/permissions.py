from rest_framework.exceptions import NotFound
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS and getattr(
                    request.user, "is_authenticated", False)
            )
            or (request.user and request.user.is_staff)
        )


def allow_only_actions(*allowed_actions):
    class _AllowOnly(BasePermission):
        def has_permission(self, request, view):
            if getattr(view, "action", None) in allowed_actions:
                return True
            raise NotFound("Not found.")

    return _AllowOnly
