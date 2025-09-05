from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        # Admins always have full access
        if user and user.is_staff:
            return True

        # Authenticated users can read (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS and user and user.is_authenticated:
            return True

        # Authenticated users can POST only to OrderViewSet
        if (
            request.method == "POST"
            and user
            and user.is_authenticated
            and view.__class__.__name__ == "OrderViewSet"
        ):
            return True

        return False
