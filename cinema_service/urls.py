from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/user/", include(("user.urls", "user"), namespace="user")),
    path("api/cinema/",
         include(("cinema.urls", "cinema"), namespace="cinema")),
    path("__debug__/", include("debug_toolbar.urls")),
]
