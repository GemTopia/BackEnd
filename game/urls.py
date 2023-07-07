from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path("<int:game_id>/", views.GameView.as_view(), name="game_detail"),
    path("play/", views.GameResult.as_view(), name="game_end"),
]
