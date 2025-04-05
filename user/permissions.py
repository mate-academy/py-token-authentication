from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if user and user.is_staff:
            return True

        if user and user.is_authenticated and request.method in SAFE_METHODS:
            return True

        return False


class IsOrderOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.user == request.user
