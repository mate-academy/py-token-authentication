from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Require authentication for all requests
        if not request.user or not request.user.is_authenticated:
            return False
        # Authenticated users can read
        if request.method in SAFE_METHODS:
            return True
        # Only staff can perform write operations (POST/PUT/PATCH)
        # DELETE is blocked at the view level
        return request.user.is_staff
