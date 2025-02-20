from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """
    The request is authenticated as admin, or is authenticated a read-only request.
    """

    def has_permission(self, request, view):
        if request.method == "POST":
            raise MethodNotAllowed('POST')

        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)

        if request.user and request.user.is_staff:
            return True

        if request.user and request.user.is_authenticated:
            if request.method in ['PUT', 'PATCH']:
                return view.get_object() == request.user
        return False
