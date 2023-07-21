from django.urls import path, include
from users.views import UserRegistration, ProfileView, LinkView, ChangePasswordView, LogoutView, \
    CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'users'
urlpatterns = [

    path("register/", UserRegistration.as_view(), name="register"),
    # path('login/', TokenObtainPairView.as_view(), name='login'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/link/', LinkView.as_view(), name='social_links'),
    path("change_password/", ChangePasswordView.as_view(), name="change_password"),
    path('logout/', LogoutView.as_view(), name='logout'),

]
