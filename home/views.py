from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from game.models import PlayedGame, Game, DailyPlayedGame
from users.models import User
from game.serializers import GameSerializer, DailyPlayedGameSerializer
from users.serializers import UserRankSerializer


class HomeView(APIView):
    serializer_class = {
        'recent_games': DailyPlayedGameSerializer,
        'ranking_games': GameSerializer,
        'top_players': UserRankSerializer,
        'all_players': UserRankSerializer,
    }

    def get(self, request):
        user = request.user
        played_games = PlayedGame.objects.filter(user=user).order_by('updated_at')
        daily_played_games = DailyPlayedGame.objects.filter(user=user).order_by('updated_at')
        all_played_games = played_games.union(daily_played_games).order_by('-updated_at')
        recent_games_serializer = DailyPlayedGameSerializer(all_played_games)

        ranking_games = Game.objects.order_by('num_of_like')
        ranking_games_serializer = GameSerializer(instance=ranking_games, many=True)

        all_players = User.objects.all()
        all_players_serializer = UserRankSerializer(instance=all_players, many=True)

        top_players = all_players.filter(hide_button=False).order_by('total_gemyto')[:20]
        top_players_serializer = UserRankSerializer(instance=top_players, many=True)
        serialized_data = {
            'recent_games': recent_games_serializer.data,
            'ranking_games': ranking_games_serializer.data,
            'top_players': top_players_serializer.data,
            'all_players': all_players_serializer.data,
        }

        return Response(serialized_data)
