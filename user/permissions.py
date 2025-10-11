from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    IsAdminUser,
    SAFE_METHODS
)


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return IsAuthenticated().has_permission(request, view)

        return IsAdminUser().has_permission(request, view)
