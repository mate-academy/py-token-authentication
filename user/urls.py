from django.urls import path
from .views import CreateUserView, LoginUserView

app_name = "user"

urlpatterns = [
    path("register/", 
         CreateUserView.as_view(), name="register"),
    path('login/', 
         LoginUserView.as_view(), name="token-auth")
]