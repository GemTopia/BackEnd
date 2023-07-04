from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from game.models import PlayedGame, Game
from users.models import User
from game.serializers import GameSerializer
from rest_framework import filters


class HomeView(APIView):
    """
        recent_games , ranking_game , ranking_players
    """

    serializer_class = GameSerializer

    def get(self, request):
        user = request.user
        recent_games = PlayedGame.objects.filter(user=user).order_by('-updated_at')
        ranking_games = Game.objects.all()
        # ranking_playes=User.objects.all()

        recent_games_serializer = GameSerializer(instance=recent_games, many=True)
        ranking_games_serializer = GameSerializer(instance=ranking_games, many=True)
        # ranking_playes_serializer=
        serialized_data = {
            'recent_games': recent_games_serializer.data,
            'ranking_games': ranking_games_serializer.data
        }

        return Response(serialized_data)
