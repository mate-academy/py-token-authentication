from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            view.__class__.__name__ == "OrderViewSet"
            and request.method == "POST"
            and request.user
            and request.user.is_authenticated
        ) or (
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        ) or (
            request.user
            and request.user.is_staff
        )
