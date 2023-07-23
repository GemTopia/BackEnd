from django.urls import path, include
from landing.views import NewsViewSet,JustEndpoint

app_name = 'landing'
urlpatterns = [

    path("", NewsViewSet.as_view(), name="landing"),
    path("learn_more/",JustEndpoint.as_view(),name="lean_more"),
    path("terms_of_use/",JustEndpoint.as_view(),name="terms_of_use"),

]
