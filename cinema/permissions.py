from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return (
            request.method in SAFE_METHODS and request.user.is_authenticated
        ) or request.user.is_staff
