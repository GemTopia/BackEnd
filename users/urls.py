from django.urls import path, include
from users.views import UserRegistration
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

router = DefaultRouter()
router.register('', UserViewSet, basename='user')

app_name = 'users'
urlpatterns = [
    path("register/", UserRegistration.as_view(), name="register"),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]

