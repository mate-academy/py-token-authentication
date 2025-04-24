from rest_framework.authentication import TokenAuthentication

from user.permissions import IsAdminOrIfAuthenticatedReadOnly


class DefaultAuthMixin:
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
