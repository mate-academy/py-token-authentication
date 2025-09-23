from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        from cinema.views import OrderViewSet
        user = request.user

        if user and user.is_staff:
            return True

        if not user or not user.is_authenticated:
            return False

        if isinstance(view, OrderViewSet):
            return (request.method in permissions.SAFE_METHODS
                    or request.method == "POST")

        return request.method in permissions.SAFE_METHODS
