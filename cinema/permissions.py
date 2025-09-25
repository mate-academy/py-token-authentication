from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        if (request.method == "POST"
                and view.__class__.__name__ == "OrderViewSet"):
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)
