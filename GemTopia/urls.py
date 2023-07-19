from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers
from landing.views import NewsViewSet


urlpatterns = [
    path('admin/', admin.site.urls),

    # Swagger & Redoc UI:
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Apps urls:

    path("users/", include('users.urls', namespace='users')),
    path("game/", include('game.urls', namespace='game')),
    path("home/", include('home.urls', namespace='home')),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path("", include('landing.urls', namespace='landing')),

]


