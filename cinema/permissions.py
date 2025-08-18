from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True
        if request.method == "POST" and request.user.is_authenticated:
            if view.__class__.__name__ == "OrderViewSet":
                return True
        return False
