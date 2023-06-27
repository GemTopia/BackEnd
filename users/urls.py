from django.urls import path
from users.views import UserRegistration
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'users'
urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

