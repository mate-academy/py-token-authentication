from rest_framework import permissions


class IsAdminOrIfAuthenticatedReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Allow access if the user is a superuser or staff.
        if request.user and (request.user.is_superuser or request.user.is_staff):
            return True

        # Handle viewsets that have a 'basename' attribute.
        if hasattr(view, 'basename'):
            # For the "order" viewset, allow any authenticated user to create or read.
            if view.basename == "order":
                if request.method in permissions.SAFE_METHODS:
                    return request.user and request.user.is_authenticated
                elif request.method == "POST":
                    return request.user and request.user.is_authenticated
                # For PUT, DELETE, etc., authenticated users do not have permission.
                return False

        # For all other views (like ManageUserView), allow read-only access for anyone.
        if request.method in permissions.SAFE_METHODS:
            return True

        # By default, deny permission for any other case.
        return False
