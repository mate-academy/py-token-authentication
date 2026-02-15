from rest_framework.permissions import BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """Allow only admins to modify objects, others can only read"""

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return obj == request.user
