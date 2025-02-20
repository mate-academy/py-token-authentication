from django.urls import path
from user.views import UserCreateView, LoginView, UserUpdateView


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path('login/', LoginView.as_view(), name="login"),
    path("me/",UserUpdateView.as_view(), name="manage" )
]

app_name = "user"
