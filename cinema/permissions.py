from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        if request.method == "POST":
            return request.user and request.user.is_staff
        return True


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrReadOnlyStrict(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class IsAdminForPostOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user and request.user.is_staff
        return True
