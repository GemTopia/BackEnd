from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import GameSerializer, ScoresSerializer, DailyPlayedGameSerializer
from rest_framework.response import Response
from .models import Game, DailyPlayedGame


class GameView(APIView):
    """"
        GameDetail
    """
    serializer_class = GameSerializer

    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        game_serializer = GameSerializer(instance=game)
        scores = game.game_scores
        score_serializer = ScoresSerializer(instance=scores)
        players_score_list = DailyPlayedGame.objects.order_by('score')
        players_list_serializer = DailyPlayedGameSerializer(instance=players_score_list, many=True)

        serialized_data = {
            'game': game_serializer.data,
            'scores': score_serializer.data,
            'players_list': players_list_serializer
        }
        return Response(serialized_data.data)
