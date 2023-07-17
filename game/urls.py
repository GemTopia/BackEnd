from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path("detail/<int:game_id>/", views.GameView.as_view(), name="game_detail")
]
