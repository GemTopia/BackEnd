from .serializers import GameSerializer, ScoresSerializer, DailyPlayedGameSerializer, ReportSerializer, LikeSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Game, DailyPlayedGame, Like
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

first_level_token = 0.05 * 10
second_level_token = 0.15 * 10
third_level_token = 0.25 * 10
fourth_level_token = 0.55 * 10


class GameView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = {
        'game': GameSerializer,
        'scores': ScoresSerializer,
        'players_list': DailyPlayedGameSerializer,
    }

    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        game_serializer = GameSerializer(instance=game, context={'request': request})

        scores = game.scores
        score_serializer = ScoresSerializer(instance=scores)

        players_score_list = DailyPlayedGame.objects.filter(game=game).order_by('-score')
        players_list_serializer = []
        for player in players_score_list:
            user_data = {
                'id': player.user.id,
                'user_name': player.user.user_name,
                'avatar': None,
                'score': player.score,
            }
            if player.user.avatar:
                user_data['avatar'] = player.user.avatar.url
            players_list_serializer.append(user_data)

        serialized_data = {
            'game': game_serializer.data,
            'scores': score_serializer.data,
            'players_list': players_list_serializer
        }
        return Response(serialized_data)


class GameResult(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DailyPlayedGameSerializer

    def post(self, request):
        user = request.user
        result_game = self.serializer_class(data=request.data)
        result_game.is_valid(raise_exception=True)
        game = result_game.validated_data['game']
        result_game.validated_data['user'] = user
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
                result_game.validated_data['game_gemyto'] = gemyto
                result_game.validated_data['state'] = state + 1
                daily_played.game_gemyto = gemyto + daily_played.game_gemyto
                daily_played.state = state + 1
            if result_game.validated_data['score'] > daily_played.score:
                daily_played.score = result_game.validated_data['score']
                result_game.validated_data['is_new_record'] = True
            daily_played.save()
            return Response(result_game.data, status=status.HTTP_200_OK)
        else:
            if result_game.is_valid():
                if result_game.validated_data['score'] > game_scores.first_level_score:
                    result_game.validated_data['game_gemyto'] = 0.5
                    result_game.validated_data['state'] = 1
                    result_game.validated_data['is_new_record'] = True
                result_game.save()
                return Response(result_game.data, status=status.HTTP_200_OK)
            return Response(result_game.data, status=status.HTTP_400_BAD_REQUEST)


class GameLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeSerializer

    def get(self, request, game_id):
        game = Game.objects.get(pk=game_id)
        user = request.user
        like, created = Like.objects.get_or_create(game=game, user=user)

        if not created:
            like.delete()
            is_liked_by_user = False
        else:
            is_liked_by_user = True

        response_data = {
            'like': LikeSerializer(like).data,
            'is_liked_by_user': is_liked_by_user,
        }

        return Response(response_data)


class ReportView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReportSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
