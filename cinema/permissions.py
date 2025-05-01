from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, "user"):
            return False
        return bool(
            request.user.is_staff
            or obj.user == request.user
        )
