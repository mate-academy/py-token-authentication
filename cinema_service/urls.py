# cinema_service/urls.py

from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/login/", ObtainAuthToken.as_view(), name="user-login"),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/cinema/", include("cinema.urls", namespace="cinema")),
    path("__debug__/", include("debug_toolbar.urls")),
]
