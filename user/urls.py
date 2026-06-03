from django.urls import path

from user.views import UserCreateAPIView

app_name = "user"

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="create")
]
