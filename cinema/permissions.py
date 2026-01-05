from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if user is None:
            return False

        return (
            user.is_staff
            or (
                request.method in SAFE_METHODS
                and user.is_authenticated
            )
        )
