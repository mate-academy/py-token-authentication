from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cinema/", include("cinema.urls", namespace="cinema")),
    path("api/cinema/user/", include("user.urls", namespace="user")),
    path("__debug__/", include("debug_toolbar.urls")),
]
