from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        if request.method == "POST":
            return bool(request.user and request.user.is_staff)

        return False

    def has_object_permission(self, request, view, obj):
        return False


class ListCreateRetrievePermission(IsAdminOrIfAuthenticatedReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return bool(
                request.user and (
                    request.user.is_authenticated or request.user.is_staff
                )
            )

        return False


class AllowAllForAdmin(IsAdminOrIfAuthenticatedReadOnly):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class ListCreateAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS + ("POST",):
            return bool(request.user and request.user.is_authenticated)
        return False

    def has_object_permission(self, request, view, obj):
        return False
