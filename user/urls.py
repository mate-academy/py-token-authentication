# write your code here
from django.urls import path

from .views import AuthUserViewSet

app_name = 'user'

urlpatterns = [
    path('login/', AuthUserViewSet.as_view(), name='login_token'),
]
