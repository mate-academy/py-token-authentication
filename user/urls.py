from django.urls import path

from user.views import CreateUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create")
]

app_name = "user"
