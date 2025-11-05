from django.http import Http404
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import status


class MethodNotAllowed(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = "Method not allowed."
    default_code = "method_not_allowed"


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user
                and request.user.is_authenticated
            )
            or (
                request.user
                and request.user.is_staff
            )
        )


class GetOrCreatePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in ["POST", "GET"]:
            return True
        raise MethodNotAllowed


class GetListOrCreatePermission(BasePermission):

    def has_permission(self, request, view):
        if request.method == "POST" or view.action == "list":
            return True
        raise Http404
