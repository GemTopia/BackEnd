from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from landing.models import GemytoInfo
from django.http import JsonResponse
import requests
import json




class Landing(APIView):
    def get(self,request):
        headers = {'X-CoinAPI-Key': ''}
        response = requests.get('https://rest.coinapi.io/v1/assets/ring', headers=headers,)
        return Response(response)
        