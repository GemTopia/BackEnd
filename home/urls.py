from . import views
from django.urls import include, path
app_name = 'home'
urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),



]
