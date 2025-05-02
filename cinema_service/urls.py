from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls")),
    path("api/cinema/", include("cinema.urls", namespace="cinema")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/", include("rest_framework.urls")),
]
