from rest_framework.permissions import (BasePermission,
                                        SAFE_METHODS)


class IsAdminOrIfAuthenticatedReadOnly(
    BasePermission
):
    def has_permission(self, request, view):
        if request.method in ("HEAD", "OPTIONS"):
            return True

        user = request.user

        if user and user.is_staff:
            return True

        view_name = getattr(
            view,
            "basename",
            ""
        ) or view.__class__.__name__.lower()
        if "order" in view_name:
            if request.method in SAFE_METHODS or request.method == "POST":
                return user and user.is_authenticated
            return False

        if request.method in SAFE_METHODS:
            return user and user.is_authenticated

        return False
