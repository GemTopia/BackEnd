from rest_framework.views import APIView
from django.core.mail import send_mail
from game.models import Game
from game.serializers import GameSerializer
from .models import EmailForNews, GemytoInfo
from .serializers import NewsSerializer, GemInfoSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import requests


class NewsViewSet(APIView):
    def post(self, request, *args, **kwargs):
        if EmailForNews.objects.filter(email=request.data['email']).exists():
            raise ValueError("This email has already been registered")
        ser_data = NewsSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
        else:
            return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def get(self, request):
        now = datetime.now()
        top_3_games = Game.objects.order_by('-num_of_like')[:3]
        serialized_top_3_games = GameSerializer(instance=top_3_games, many=True)

        if GemytoInfo.objects.filter().exists():
            latest_record = GemytoInfo.objects.latest('created_at')
            if latest_record.created_at.date() == now.date() and latest_record.created_at.hour == now.hour and latest_record.created_at.minute + 15 >= now.minute:
                serialized_ans = GemInfoSerializer(instance=latest_record)
                json_ans = {'token': serialized_ans.data}
                json_ans['top_3_games'] = serialized_top_3_games.data
                return Response(json_ans)
            else:
                headers = {'X-CoinAPI-Key': 'C0BBD2E3-A3B0-4D69-9A2D-73FCF9EBB67F'}
                response = requests.get('https://rest.coinapi.io/v1/assets/ring', headers=headers)
                data = {
                    'token_value': response.json()[0],
                }
                ser_data = GemInfoSerializer(data=data)
                if ser_data.is_valid():
                    ser_data.create(ser_data.validated_data)
                else:
                    return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
                ans = GemytoInfo.objects.latest('created_at')
                serialized_ans = GemInfoSerializer(instance=ans)
                json_ans = {'token': serialized_ans.data}
                return Response(json_ans)

        else:
            headers = {'X-CoinAPI-Key': 'C0BBD2E3-A3B0-4D69-9A2D-73FCF9EBB67F'}
            response = requests.get('https://rest.coinapi.io/v1/assets/ring', headers=headers)
            data = {
                'token_value': response.json()[0],
            }
            ser_data = GemInfoSerializer(data=data)
            if ser_data.is_valid():
                ser_data.create(ser_data.validated_data)
            else:
                return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
            ans = GemytoInfo.objects.latest('created_at')
            serialized_ans = GemInfoSerializer(instance=ans)
            json_ans = {
                'token': serialized_ans.data,
            }

        json_ans['top_3_games'] = serialized_top_3_games.data

        return Response(json_ans)
