from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        if request.user.is_authenticated and request.method == "POST" and view.__class__.__name__ == "OrderViewSet":
            return True
        return bool(request.user and request.user.is_staff)
