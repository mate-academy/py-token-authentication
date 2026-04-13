from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """Read-only for authenticated users, with scoped extra writes."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff or request.method in SAFE_METHODS:
            return True

        if view.__class__.__name__ == "ManageUserView":
            return True

        return (
            view.__class__.__name__ == "OrderViewSet"
            and request.method == "POST"
        )
