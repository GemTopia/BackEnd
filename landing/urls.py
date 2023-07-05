from django.urls import path
from landing.views import Landing
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = 'landing'
urlpatterns = [
    path("", Landing.as_view(), name="register"),
    ]

