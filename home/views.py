from itertools import groupby
from rest_framework.views import APIView
from rest_framework.response import Response
from game.models import PlayedGame, Game, DailyPlayedGame
from game.serializers import GameSerializer, DailyPlayedGameSerializer
from rest_framework.permissions import IsAuthenticated
from users.serializers import UserRankSerializer
from users.models import User


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = {
        'recent_games': DailyPlayedGameSerializer,
        'ranking_games': GameSerializer,
        'top_players': UserRankSerializer,
        'all_players': UserRankSerializer,
        'user_profile': UserRankSerializer,
    }

    def get(self, request):
        user = request.user
        user_profile = User.objects.get(user_name=user.user_name)
        user_profile_serializer = UserRankSerializer(instance=user_profile, many=False)
        copy_of_data = user_profile_serializer.data
        copy_of_data['total_gemyto'] = 0
        copy_of_data.pop('hide_button')
        copy_of_data.pop('avatar')

        played_games = PlayedGame.objects.filter(user=user).order_by('updated_at')
        daily_played_games = DailyPlayedGame.objects.filter(user=user).order_by('updated_at')
        recent_games_played = [played_game.game for played_game in played_games]
        recent_games_daily = [daily_played_game.game for daily_played_game in daily_played_games]
        recent_games = recent_games_played + recent_games_daily
        recent_games_serializer = GameSerializer(recent_games, context={'user': user}, many=True)

        ranking_games = Game.objects.order_by('-num_of_like')
        ranking_games_serializer = GameSerializer(instance=ranking_games, context={'user': user}, many=True)

        all_players = User.objects.all()
        all_players_serializer = UserRankSerializer(instance=all_players, many=True)

        top_players = all_players.filter(hide_button=False).order_by('total_gemyto')[:20]
        top_players_serializer = UserRankSerializer(instance=top_players, many=True)

        for player_data in all_players_serializer.data:
            if player_data not in top_players_serializer.data and player_data['hide_button'] is False:
                player_data['total_gemyto'] = 0
        serialized_data = {
            'recent_games': recent_games_serializer.data,
            'ranking_games': ranking_games_serializer.data,
            'top_players': top_players_serializer.data,
            'all_players': all_players_serializer.data,
            'user_profile': copy_of_data,
        }

        return Response(serialized_data)


class GamesView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GameSerializer

    def get(self, request):
        user=request.user
        sort_by = request.GET.get('sort_by', 'rate')
        if sort_by == 'earliest':
            games_sorted = Game.objects.all().order_by('created_at')
        elif sort_by == 'latest':
            games_sorted = Game.objects.all().order_by('-created_at')
        elif sort_by == 'rate':
            games_sorted = Game.objects.all().order_by('-num_of_like')
        elif sort_by == 'category':
            games = Game.objects.all().order_by('game_type',
                                                'name')
            grouped_games = {}
            for game_type, games_group in groupby(games, key=lambda game: game.game_type):
                grouped_games[game_type] = [GameSerializer(game, context={'user': user}).data for game in
                                            games_group]

            return Response(grouped_games)
        else:
            games_sorted = Game.objects.all()
        serializer = GameSerializer(games_sorted, context={'user': user}, many=True)
        return Response(serializer.data)
