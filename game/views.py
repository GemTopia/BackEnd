from .serializers import GameSerializer, ScoresSerializer, DailyPlayedGameSerializer, ReportSerializer
from .models import Game, DailyPlayedGame, Report
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework import status
from django.conf import settings

first_level_token = 0.05 * 10
second_level_token = 0.15 * 10
third_level_token = 0.25 * 10
fourth_level_token = 0.55 * 10


class GameView(APIView):
    serializer_class = {
        'game': GameSerializer,
        'scores': ScoresSerializer,
        'players_list': DailyPlayedGameSerializer,
    }

    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        game_serializer = GameSerializer(instance=game)
        scores = game.scores
        score_serializer = ScoresSerializer(instance=scores)
        players_score_list = DailyPlayedGame.objects.order_by('score')
        players_list_serializer = DailyPlayedGameSerializer(instance=players_score_list, many=True)

        serialized_data = {
            'game': game_serializer.data,
            'scores': score_serializer.data,
            'players_list': players_list_serializer.data
        }
        return Response(serialized_data)


class GameResult(APIView):
    serializer_class = DailyPlayedGameSerializer

    def post(self, request):
        result_game = self.serializer_class(data=request.data)
        result_game.is_valid(raise_exception=True)
        game = result_game.validated_data['game']
        user = result_game.validated_data['user']
        game_scores = game.scores

        if DailyPlayedGame.objects.filter(game=game, user=user).exists():
            daily_played = DailyPlayedGame.objects.get(game=game, user=user)
        else:
            daily_played = None

        level_scores = {
            0: game_scores.first_level_score,
            1: game_scores.second_level_score,
            2: game_scores.third_level_score,
            3: game_scores.fourth_level_score,
        }
        level_tokens = {
            0: first_level_token,
            1: second_level_token,
            2: third_level_token,
            3: fourth_level_token,
        }

        if daily_played is not None and result_game.is_valid():
            state = daily_played.state
            level_score = level_scores.get(state)
            result_game.validated_data['state'] = state
            if state < 4 and result_game.validated_data['score'] > level_score:
                gemyto = level_tokens.get(state)
                result_game.validated_data['gemyto'] = gemyto
                result_game.validated_data['state'] = state + 1
                daily_played.gemyto = gemyto + daily_played.gemyto
                daily_played.state = state + 1
            if result_game.validated_data['score'] > daily_played.score:
                daily_played.score = result_game.validated_data['score']
            daily_played.save()
            return Response(result_game.data, status=status.HTTP_200_OK)
        else:
            if result_game.is_valid():
                if result_game.validated_data['score'] > game_scores.first_level_score:
                    result_game.validated_data['gemyto'] = 0.5
                    result_game.validated_data['state'] = 1
                result_game.save()
                return Response(result_game.data, status=status.HTTP_200_OK)
            return Response(result_game.data, status=status.HTTP_400_BAD_REQUEST)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        report = serializer.save()
        user = report.user
        send_mail(
            subject='Your report is being processed',
            message='Thank you for submitting your report. We are currently processing it.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
