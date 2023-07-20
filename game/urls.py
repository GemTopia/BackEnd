from django.urls import path
from . import views

app_name = 'game'
urlpatterns = [
    path("<int:game_id>/", views.GameView.as_view(), name="game_detail"),
    path("result/", views.GameResult.as_view(), name="game_end"),
    path("like/<int:game_id>/", views.GameLikeView.as_view(), name="like_game"),
    path("report/", views.ReportView.as_view(), name="report"),

]
