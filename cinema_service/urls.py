from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cinema/",
         include(("cinema.urls", "cinema"), namespace="cinema")),
    path("api/user/",
         include(("user.urls", "user"), namespace="user")),
]
