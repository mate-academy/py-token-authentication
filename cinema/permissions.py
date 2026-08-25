from django.urls import resolve
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        current_url = resolve(request.path_info).url_name
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or request.user.is_staff
            or (current_url == "order-list" and request.user.is_authenticated)
        )
