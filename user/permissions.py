from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_staff:
            return True
        if not request.user or not request.user.is_authenticated:
            return False

        allowed_actions = {
            "GenreViewSet": {"GET", "POST"},
            "CinemaHallViewSet": {"GET", "POST"},
            "ActorViewSet": {"GET", "POST"},
            "MovieViewSet": {"GET", "POST"},
            "MovieSessionViewSet": {"GET", "POST", "PUT", "PATCH", "DELETE"},
            "OrderViewSet": {"GET", "POST"},
        }

        view_name = view.__class__.__name__
        method = request.method

        # Get allowed methods for this view
        allowed = allowed_actions.get(view_name, set())

        return method in allowed
