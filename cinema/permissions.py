"""Role-based access for cinema resources."""
from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request

if TYPE_CHECKING:
    from rest_framework.views import APIView


class IsAdminOrIfAuthenticatedReadOnly(BasePermission):
    """Allow authenticated reads and staff-only writes."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.method in SAFE_METHODS or request.user.is_staff)
        )
