"""Root routes for the admin, user accounts, and cinema API."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/user/",
        include("user.urls", namespace="user"),
    ),
    path("api/cinema/", include("cinema.urls", namespace="cinema")),
    path("__debug__/", include("debug_toolbar.urls")),
]
