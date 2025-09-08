from rest_framework import viewsets, status
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.response import Response


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    Allows full access for admin users (is_staff).
    Allows read-only access (GET, HEAD, OPTIONS) for authenticated users.
    Denies access for unauthenticated users.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_staff


class ReadCreateOnlyViewSet(viewsets.ModelViewSet):
    """
    A base viewset that allows only list and create actions.
    All other actions (retrieve, update, partial_update, destroy) return 404.
    """
    http_method_names = [
        "get",
        "post",
        "head",
        "options",
        "put",
        "patch",
        "delete"
    ]

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
