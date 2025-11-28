from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True

        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated

        return False


class RegularAuthenticatedUsers(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list"]:
            return request.user and request.user.is_authenticated
        elif view.action in ["create"]:
            return request.user and request.user.is_staff
        elif view.action in ["destroy"]:
            return False
        return False


class OrderAuthenticatedUsers(BasePermission):
    def has_permission(self, request, view):
        if view.action in ["list", "create"]:
            return request.user and request.user.is_authenticated
        elif view.action in ["destroy"]:
            return False
        return False


class Denied(BasePermission):
    def has_permission(self, request, view):
        return False
