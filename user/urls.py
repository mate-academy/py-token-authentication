from django.urls import path

from user.views import CreateUserView, CreateTokenView, DetailUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path('login/', CreateTokenView.as_view(), name="login"),
    path('me/', DetailUserView.as_view(), name="manage"),
]

app_name = "user"
