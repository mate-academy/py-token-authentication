from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request: Request, view) -> bool:
        return bool(
            request.user.is_staff
        ) or bool(
            request.method in SAFE_METHODS and request.user.is_authenticated
        )
