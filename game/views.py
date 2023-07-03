from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import GameSerializer
from rest_framework.response import Response
from .models import Game


class GameView(APIView):
    """"
        GameDetail
    """
    serializer_class = GameSerializer

    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        serializer = GameSerializer(instance=game)
        return Response(serializer.data)
