from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

# class IsAdminOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_staff)
#
#
# class IsOrderOwner(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return obj.user == request.user or request.user.is_staff


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
