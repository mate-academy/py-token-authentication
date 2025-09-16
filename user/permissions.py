from rest_framework.permissions import (
    BasePermission,
    IsAuthenticated,
    IsAdminUser,
    SAFE_METHODS
)


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        action = getattr(view, "action", None)
        route_name = request.resolver_match.view_name
        if action in ["list", "retrieve"]:
            return IsAuthenticated().has_permission(request, view)
        if not action:
            if request.method in SAFE_METHODS:
                return IsAuthenticated().has_permission(request, view)
            elif (request.method == "POST"
                  and route_name == "cinema:order-list"):
                return IsAuthenticated().has_permission(request, view)
        return IsAdminUser().has_permission(request, view)
