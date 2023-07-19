from django.urls import path, include
from landing.views import NewsViewSet

app_name = 'landing'
urlpatterns = [

    path("landing/", NewsViewSet.as_view(), name="landing"),

]
