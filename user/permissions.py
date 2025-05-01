from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        return (
            request.method in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
        )


class NoDeletePermission(BasePermission):

    def has_permission(self, request, view):
        return request.method != "DELETE"

    def has_object_permission(self, request, view, obj):
        return request.method != "DELETE"


class NoUnsafeMethodsPermission(BasePermission):

    def has_permission(self, request, view):
        return request.method in ("GET", "POST")

    def has_object_permission(self, request, view, obj):
        return request.method in ("GET", "POST")
